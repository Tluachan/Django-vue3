from rest_framework import serializers

from .models import Category, Product, Review, FavoriteShop

from djoser.serializers import UserCreateSerializer,UserSerializer
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',     
        )

#add field during user creation
class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 'is_staff')

class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'is_staff']
    
    def to_representation(self, instance):
        print('Converting user instance to representation...')
        return super().to_representation(instance)

class ProductForReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "address",
            "get_absolute_url",
            "phone",
            "map_url",
            "avg_rating",
            "get_image",
            "get_thumbnail",
        )

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductForReviewSerializer(read_only=True)
    class Meta:
        model = Review
        read_only_fields = (
            'user',
            'datetime',
        ),
        fields = (
            'id',
            'content',
            'rating',
            'user',
            'datetime',
            'product',
        )

    def create(self, validated_data):
        return Review.objects.create(**validated_data)   

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "address",
            "get_absolute_url",
            "phone",
            "map_url",
            "avg_rating",
            "get_image",
            "get_thumbnail",
            "reviews"
        )

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
            "get_image",
            "get_thumbnail",
        )


class FavoriteShopSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductForReviewSerializer(read_only=True)

    class Meta:
        model = FavoriteShop
        read_only_fields =(
            'user',
            'product',
        )
        fields = (
            'id',
            'user',
            'product',
        )
    def create(self, validated_data):
        return FavoriteShop.objects.create(**validated_data)