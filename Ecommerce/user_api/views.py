from django.shortcuts import render,redirect

from .serializers import (UserRegisterSerializer,
                          CartItemSerializer,
                          OrderSerializer)

from admin_api.serializers import (CategorySerializer,
                                    ProductSerializer)

from .models import (User,
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

from django_filters.rest_framework import DjangoFilterBackend




#..........................USER REGISTRATION AND MAIL SENDING..................................#

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

            email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            email.attach_alternative(html_content, "text/html")
            email.send()

            data['response'] = 'message:User created'
            refresh = RefreshToken.for_user(account)
        else:
            data = serializer.errors
        return Response(data)

        
#..........................LIST OF PRODUCTS..................................#

class UserProductlistview(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product_name','price','quantity','categories']


#__USERS view specific Products__#


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



#..........................ADD TO CART..................................#



class AddToCartView(generics.CreateAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CartItemSerializer


    def post(self, request, *args, **kwargs):
        product = int(request.data.get('product'))
        quantity = int(request.data.get('quantity'))
        user = request.user

        try:
            product = Product.objects.get(id=product)
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

        cart_item.total = product.price * cart_item.quantity
        cart_item.save()

        cart_total = CartItem.objects.filter(user=user).aggregate(total_amount=Sum('total'))['total_amount']
        serializer = CartItemSerializer(cart_item)
        context = {
            "cart_items": serializer.data,
            "cart_total": cart_total

        }
        return Response(context)


class CartListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = CartItemSerializer


    def get_queryset(self):
        user = self.request.user
        return CartItem.objects.filter(user=user)
        


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
        order = Order.objects.create(user=user, total_amount=total_amount, status='pending')

        for cart_item in cart_items:
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

            cart_item.product.quantity -= cart_item.quantity
            cart_item.product.save()

            cart_item.delete()
        
        
        context =  {'user': user,
                    'total_amount': total_amount,
                    'status': order.status}

        subject = 'Your Order Placed Successfully'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        html_content = render_to_string('order_user.html',context)
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()


        

        serializer = self.get_serializer(order)
        return Response(serializer.data)



class OrderListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset= Order.objects.all()
    serializer_class= OrderSerializer
    # pagination_class=MyCustomPagination
    

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)




