from rest_framework import serializers
from .models import Category,Product
from user_api.models import User,Order



class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id', 'category_name', 'image', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
     

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'description', 'price','quantity','image','categories','created_at']


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name','last_name']

    
class OrderUpdateSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Order
        fields = ['id' ,'user','status']