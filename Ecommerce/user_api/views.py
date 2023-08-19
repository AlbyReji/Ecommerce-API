from django.shortcuts import render,redirect

from .serializers import (UserRegisterSerializer,
                          PasswordResetRequestSerializer,
                          PasswordResetSerializer,
                          AddressSerializer,
                          ProfileSerializer,
                          CartItemSerializer,
                          OrderSerializer,
                          OrderlistSerializer)

from admin_api.serializers import (CategorySerializer,
                                    ProductSerializer)

from .models import (User,
                    Address,
                    UserProfile,
                    CartItem,
                    Order,
                    OrderItem)

from admin_api.models import (Category,
                              Product)


from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import generics,serializers
from rest_framework.generics import  RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from django.db.models import Sum

from django.core.mail import send_mail
from django.conf import settings
from Ecommerce.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags 
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

from django_filters.rest_framework import DjangoFilterBackend
from .pagination import NumberPagination




#__User: API for user Registration and mail Sending__#

class RegisterView(APIView):

    def post(self, request, format=None):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save() 
            
            subject = 'User Registration'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [account.email]

            html_content = render_to_string('user_register.html', {'username': account.username})
            text_content = strip_tags(html_content)

            try:
                email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
                email.attach_alternative(html_content, "text/html")
                email.send()

                data['response'] = 'message:User created'
                refresh = RefreshToken.for_user(account)
            except Exception as e:
                data['error'] = 'An error occurred while sending the registration email.'
                return Response(data)   
        else:
            data = serializer.errors
        return Response(data)

#__User: API for Password reset and mail sending__#

class PasswordResetRequestView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email address does not exist'})
        
        access_token = AccessToken.for_user(user)
        reset_url = reverse('password_reset_verify') + f'?token={access_token}'
        
        subject = 'Password Reset Request'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        context = {'reset_url': reset_url}  
        html_content = render_to_string('password_reset.html', context)
        text_content = strip_tags(html_content)
        
        try:
            email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            email.attach_alternative(html_content, "text/html")
            email.send()
            return Response({'message': 'Password reset email sent successfully'})
        except Exception as e:
            return Response({'error': 'An error occurred while sending the email'})


#__User: API for Verifying the token__#

class PasswordResetVerifyView(APIView):

    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token')
        print(token)
        if token is None:
            return Response({'error': 'Token not provided'})
        
        try:
            access_token = AccessToken(token)
            user_id = access_token.payload.get('user_id')
            user = User.objects.get(pk=user_id)
            return Response({'message': 'Token is valid'})
        except User.DoesNotExist:
            return Response({'error': 'Invalid token'})


#__User: API for Password reset__#

class PasswordResetView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = request.query_params.get('token')
        if token is None:
            return Response({'error': 'Token not provided'})
        
        try:
            access_token = AccessToken(token)
            user_id = access_token.payload.get('user_id')
            user = User.objects.get(pk=user_id)
            
            password = serializer.validated_data['password']
            user.set_password(password)
            user.save()
            
            return Response({'message': 'Password reset successfully'})
        except User.DoesNotExist:
            return Response({'error': 'Invalid token'})


#__Users: Api for address__#

class AddressCreateview(generics.ListCreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        user = self.request.user
        return Address.objects.filter(user=user)
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({"Address is added"})

#__Users: API for Retrieve,update and delete Address__#

class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_queryset(self):
        user = self.request.user
        return Address.objects.filter(user=user)

        
    def delete(self, request, *args, **kwargs):

        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Address deleted successfully."})
        except NotFound:
            return Response({"message": "Address not found."}) 


#__Users:API for create profile and view profile__#

class ProfileCreateview(generics.ListCreateAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        user = self.request.user
        return UserProfile.objects.filter(user=user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({"Profile is created"})

        
#__Users:API for view the list of categories__#

class CatgorylistView(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = NumberPagination


        
#__Users:API for view the list of products__#

class UserProductlistview(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product_name','price','quantity','categories']
    pagination_class = NumberPagination



#__Users:API for view specific Products__#

class UserProductView(generics.RetrieveAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except NotFound:
            return Response({"message": "Product not found."})


#__Users: API for add different products to the cart__#

class AddToCartView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CartItemSerializer



    def post(self, request, *args, **kwargs):
        product_id = int(request.data.get('product'))
        quantity = int(request.data.get('quantity'))
        user = request.user

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'})

        if product.quantity <= 0:
            return Response({"error": f" {product.product_name} : Out of stock"})

        cart_item, item_created = CartItem.objects.get_or_create(user=user, product=product)

        if quantity == 0:
            return Response({"error": "Quantity must be at least 1"})

        if not item_created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = int(quantity)

        if product.quantity < cart_item.quantity:
            return Response({"error": f" {product.product_name} : Quantity exceeds available stock"})

        cart_item.product_price = product.price 
        cart_item.total = product.price * cart_item.quantity
        cart_item.save()

        cart_total = CartItem.objects.filter(user=user).aggregate(total_amount=Sum('total'))['total_amount']
        serializer = CartItemSerializer(cart_item)
        context = {
            "cart_items": serializer.data,
            "cart_total": cart_total
        }
        return Response(context)

#__Users:API for view  products in the cart__#

class CartListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CartItemSerializer
    pagination_class = NumberPagination



    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)
        

#__Users: API for upadte products in the cart__#

class CartUpdateView(generics.UpdateAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):

        user = self.request.user
        return CartItem.objects.filter(user=user)
    
    def update(self,request,*args,**kwargs):

        instance =  self.get_object()
        quantity = int(request.data.get('quantity'))
        
        if quantity <=0:
            return Response({"error": "Quantity must be at least 1"})

        instance.quantity = quantity
        instance.total = instance.product.price * quantity
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


#__Users: API for delete products in the cart__#

class CartDeleteView(generics.DestroyAPIView):
    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):

        user = self.request.user
        return CartItem.objects.filter(user=user)

    def delete(self,request,*args, **kwargs):
        
        instance = self.get_object()
        instance.delete()
        return Response({"message": "Cart item removed successfully."})


#__Users:API for place order and send mail__#

class OrderView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        cart_items = CartItem.objects.filter(user=user)

        if not cart_items.exists():
            return Response({"error": "Your cart is empty."})

        total_amount = sum(item.total for item in cart_items)

        address_id = request.data.get('address_id') 

        print(f"DEBUG: address_id = {address_id}, user = {user}")

        try:
            address = Address.objects.get(id=address_id, user=user)
        except Address.DoesNotExist:
            return Response({"error": "Address not found or does not belong to the user."})

        order = Order.objects.create(user=user,
                                     total_amount=total_amount,
                                     status='pending', 
                                     address=address)

        for cart_item in cart_items:
            product_price = cart_item.product.price
            OrderItem.objects.create(order=order,
                                     product=cart_item.product,
                                     quantity=cart_item.quantity,
                                     product_price=product_price)

            cart_item.product.quantity -= cart_item.quantity
            cart_item.product.save()

            cart_item.delete()
        
        
        context =  {'user': user,
                    'total_amount': total_amount,
                    'status': order.status}

        try:
            subject = 'Your Order Placed Successfully'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            html_content = render_to_string('order_user.html',context)
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            email.attach_alternative(html_content, "text/html")
            email.send()
        except Exception as user_email_error:
            return Response({"error": f"Failed to send user email: {user_email_error}"})
        
        try:
            subject="New Order Received"
            from_email = settings.EMAIL_HOST_USER
            recipient_list=['admin@gmail.com']
            html_content=render_to_string('order_admin.html',context)
            text_content = strip_tags(html_content)
            email=EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            email.attach_alternative(html_content,"text/html")
            email.send()
        except Exception as admin_email_error:
            return Response({"error": f"Failed to send admin email: {admin_email_error}"})

        serializer = self.get_serializer(order)
        return Response(serializer.data)


#__Users:API for view list of orders__#

class OrderListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset= Order.objects.all()
    serializer_class= OrderlistSerializer
    pagination_class=NumberPagination
    

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)

#__non-registered user __#

#__non-registered user can view list of categorys__#

class NonUserCatgorylistView(generics.ListAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = NumberPagination

#__non-registered user can view list of products#

class NonUserProductlistview(generics.ListAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product_name','price','quantity','categories']
    pagination_class = NumberPagination


#__non-registered user can view details of specifiv product__#

class NonUserProductView(generics.RetrieveAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except NotFound:
            return Response({"message": "Product not found."})