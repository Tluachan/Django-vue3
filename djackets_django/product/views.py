from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db import transaction

from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Product, Category, Review, FavoriteShop
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer, UserSerializer, FavoriteShopSerializer
from .Msg import Msg

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    def create(self, request):
        print('request', request.data)
        # get the product object using the slug
        product_slug = request.data.get('product')
        #print(product_slug)
        product = get_object_or_404(Product, slug=product_slug)
        #print('product', product)
        username = request.data.get('user')

        user = get_object_or_404(User, username=username)
        print('username pass to review',user)
        # add the product object to the form data
        review = Review.objects.create(
            product=product,
            content=request.data.get('content'),
            rating=request.data.get('rating'),
            user=user
        )
        product.update_rating()
        # serialize the new Review instance and return the serialized data
        serializer = ReviewSerializer(instance=review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

class ReviewList(APIView):
    def get_object(self, product_slug):
        try:
            return Review.objects.filter(product__slug=product_slug)
        except Review.DoesNotExist:
            raise Http404
    
    def get(self, request, product_slug, format=None):
        reviews = self.get_object(product_slug)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
class UserDetail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LatestProductsList(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()[0:4]
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class ProductDetail(APIView):
    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        serializer = ProductSerializer(product)
        return Response(serializer.data) 

class CategoryDetail(APIView):
    def get_object(self, category_slug):
        try:
            return Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            raise Http404
    
    def get(self, request, category_slug, format=None):
        category = self.get_object(category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
class CategoryList(APIView):
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def search(request):
    query = request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})


class FavoriteShopViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteShopSerializer
    queryset = FavoriteShop.objects.all()

    def create(self, request):
        # get the product object using the slug
        product_slug = request.data.get('product')
        product = get_object_or_404(Product, slug=product_slug)
        username = request.data.get('user')
        user = get_object_or_404(User, username=username)
        # add the product object to the form data
        #favoriteShop, created = FavoriteShop.objects.get_or_create(
        #    product=product,user=user
        #)


        favoriteShop = FavoriteShop.objects.create(
            product=product,
            user=user
        )
        product.update_favorite_count()
        # serialize the new Review instance and return the serialized data
        serializer = FavoriteShopSerializer(instance=favoriteShop)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self,request, pk=None):
        if 'user' in request.data and 'product' in request.data:
            product_slug = request.data.get('product')
            product = get_object_or_404(Product, slug=product_slug)
            username = request.data.get('user')
            user = get_object_or_404(User, username=username)
            FavoriteShop = get_object_or_404(FavoriteShop, user=user, product=product)
        else:
            favorite_shop = get_object_or_404(FavoriteShop, pk=pk)

        favorite_shop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  

        


class FavoriteShopView(APIView):
    # get all favorite shop list
    def get(self, request):
        print(request.data)

        if 'user' not in request.data and 'product' not in request.data:
            return Response("user_id or shop_id is required.", status=status.HTTP_400_BAD_REQUEST)
        
        if 'user' in request.data:
            username = request.data.get('user')
            user = User.objects.get(username=username)
            favorite_shops = FavoriteShop.objects.filter(user=user)
        
        if 'product' in request.data:
            product_slug = request.data.get('product')
            product = Product.objects.get(slug=product_slug)
            favorite_shops = FavoriteShop.objects.filter(product=product)

        serializer = FavoriteShopSerializer(favorite_shops, many=True)
        return Msg(data = serializer.data).response()

    # add a new favorite shop
    @transaction.atomic
    def post(self, request):
        serializer = FavoriteShopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # update shop favorite count
            product_slug = request.data['product']
            product = Product.objects.get(slug=product_slug)
            product.update_favorite_count()

            return Msg(data=serializer.data).response()
        return Msg(code=400, msg=serializer.errors).response()

    # delete a favorite shop
    @transaction.atomic
    def delete(self, request):
        if 'user_id' not in request.data or 'shop_id' not in request.data:
            return Response("user_id and shop_id are required.", status=status.HTTP_400_BAD_REQUEST)
        
        user_id = request.data['user_id']
        shop_id = request.data['shop_id']
        favorite_shop = FavoriteShop.objects.filter(user_id=user_id, shop_id=shop_id)
        if not favorite_shop:
            return Msg(code = status.HTTP_404_NOT_FOUND,msg="The favorite shop is not exists.").response()
        favorite_shop.delete()

        # update shop favorite count
        shop = Shop.objects.get(id=shop_id)
        shop.update_favorite_count()
        
        return Msg(data="Delete successfully").response()
