from django.shortcuts import render,redirect

from .serializers import (CategorySerializer,
                          ProductSerializer,
                          UserListSerializer)

from .models import (Category,
                     Product)

from user_api.models import (User)



from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView 
from rest_framework import generics,serializers
from rest_framework.generics import  RetrieveAPIView
from rest_framework.permissions import IsAdminUser

from .pagination import NumberPagination


#..........................CATEGORY CREATE..................................#

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

#..........................LIST ALL CATEGORYS..................................#

class CategoryListView(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = NumberPagination


#..........................CATEGORY RETRIEVE, UPDATE AND DELETE ..................................#


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


#..........................PRODUCT CREATE..................................#

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


#..........................LIST ALL PRODUCTS..................................#

class ProductListView(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = NumberPagination


#..........................PRODUCT RETRIEVE, UPDATE AND DELETE ..................................#


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



#..........................LIST OF USERS..................................#


class UserListView(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    pagination_class = NumberPagination
    


#..........................USER DELETE ..................................#


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

