from django.contrib.auth import get_user_model;
from django.contrib.auth.password_validation import validate_password;
from rest_framework import serializers;
from rest_framework.validators import UniqueValidator;
from .models import *;
from decimal import Decimal;
from decimal import ROUND_DOWN;


User = get_user_model();


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
    
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False}
        }
        


class RegisterSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user

 
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'name', 'email']

   
class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Tag
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'author', 'price', 'summary', 'featured', 'tags', 'inv', 'image', 'digital']


class OrderSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_name', 'status', 'complete', 'transaction_id']


class OrderItemSerializer(serializers.ModelSerializer):
    
    # price = serializers.DecimalField(source='product.price', decimal_places=2, max_digits=100, coerce_to_string=True)
    # product_name = serializers.CharField(source='product.title', read_only=True)
    
    class Meta:
        model = OrderItem
        # fields = ['id', 'product', 'product_name', 'price', 'quantity', 'order', 'date_added']
        fields = '__all__'
    

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'


# {"first_name": "Patrick", "last_name": "Star", "username": "starman", "email": "patrick_star@gmail.com", "password": "hornets_cp3", "password2":"hornets_cp3"}

# {"username": "turncoat", "email": "mars_kingslayer@gmail.com", "first_name": "Gaius", "last_name": "Martius", "password": "mrneverfold", "password2": "mrneverfold"}