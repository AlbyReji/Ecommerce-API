from django.shortcuts import render,redirect

from .serializers import (CategorySerializer,
                          ProductSerializer,
                          UserListSerializer,
                          OrderUpdateSerializer)

from user_api.serializers import (OrderItemSerializer,
                                 OrderSerializer)

from .models import (Category,
                     Product)

from user_api.models import (User,
                             Order,
                             OrderItem)



from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import generics,serializers
from rest_framework.generics import  RetrieveAPIView
from rest_framework.permissions import IsAdminUser

from django.core.mail import send_mail
from django.conf import settings
from Ecommerce.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags 

from .pagination import NumberPagination



class CategoryCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Category Added Successfully"})
        return Response(serializer.errors)


class CategoryListView(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = NumberPagination




class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Category deleted successfully."})
        except NotFound:
            return Response({"message": "Category not found."})  



class ProductCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"Product Added Successfully"})
        return Response(serializer.errors)



class ProductListView(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = NumberPagination




class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "Product deleted successfully."})
        except NotFound:
            return Response({"message": "Product not found."})  





class UserListView(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    pagination_class = NumberPagination
    




class UserDeleteView(generics.DestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserListSerializer


    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({"message": "User deleted successfully."})
        except NotFound:
            return Response({"message": "User not found."})  



class OrderListView(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = NumberPagination



class OrderDetailView(generics.RetrieveAPIView):

    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        order_items = OrderItem.objects.filter(order=instance)
        order_item_data = []
        for item in order_items:
            order_item_data.append({
                'product': item.product.product_name,
                'quantity': item.quantity,
                'total': item.product.price * item.quantity
            })

        data = {
            **serializer.data,
            'order_items': order_item_data
        }

        return Response(data)



class OrderUpdateView(generics.UpdateAPIView):

    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]
    queryset = Order.objects.all()
    serializer_class = OrderUpdateSerializer
    lookup_field = 'pk' 

    def update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_order = serializer.save()

        total_amount = updated_order.total_amount

        context = {

            'order_id': updated_order.id,
            'order_status': updated_order.status,
            'total_amount': total_amount
        }

        subject = 'Order Confirmation'
        from_email = 'admin@gmail.com'
        recipient_list = [updated_order.user.email]

        html_content = render_to_string('order_confirm.html', context)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
        email.attach_alternative(html_content, "text/html")
        email.send()

        return Response({"message":"Order status is updated"})



class SendPromotionEmailView(APIView):

    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]


    def post(self, request, *args, **kwargs):
        subject = 'Special Promotion'
        from_email = settings.EMAIL_HOST_USER
        all_users = User.objects.exclude(is_staff=True)

        for user in all_users:
            recipient_list = [user.email]
            html_content = render_to_string('promotion_mail.html', {'user': user})
            text_content = strip_tags(html_content)

            email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            email.attach_alternative(html_content, "text/html")
            email.send()

        return Response({"message": "Promotion emails sent successfully to all users."})

