from rest_framework import serializers
from django.contrib.auth import get_user_model
from admin_api.models import Product
from .models import CartItem

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email","first_name","last_name", "password", "password2"]

    def save(self):
        reg = User(
            username =self.validated_data['username'],
            email = self.validated_data['email'],
            first_name =self.validated_data['first_name'],
            last_name =self.validated_data['last_name'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password should match'})
        reg.set_password(password)
        reg.save()
        return reg





class CartItemSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.username') 
    
    class Meta:
        model = CartItem
        fields = ['id','user', 'product', 'quantity', 'total']