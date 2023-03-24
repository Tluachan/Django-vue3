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
from rest_framework.exceptions import NotFound

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
    
class UserAllReviewList(APIView):
    def get_object(self, username):
        user = User.objects.get(username=username)
        print(user)
        try:
            return Review.objects.filter(user=user)
        except Review.DoesNotExist:
            raise Http404('This user has no review')
    
    def get(self, request, username, format=None):
        print('user all review list')
        print('username', username)
        reviews = self.get_object(username)
        print(reviews)
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

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

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
        #print('create')
        #print(request.data)
        product_slug = request.data.get('product')
        product = get_object_or_404(Product, slug=product_slug)
        username = request.data.get('user')
        user = get_object_or_404(User, username=username)

        favoriteShop, created = FavoriteShop.objects.get_or_create(
            product=product,user=user
        )

        #favoriteShop = FavoriteShop.objects.create(
        #    product=product,
        #    user=user
        #)
        if created:
            product.update_favorite_count()
            
        # serialize the new Review instance and return the serialized data
        serializer = FavoriteShopSerializer(instance=favoriteShop)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def destroy(self, request, pk=None):
        print('call destroy')
        print(request.data)
        if 'user' in request.data and 'product' in request.data:
            print('if check')
            product_slug = request.data.get('product')
            product = get_object_or_404(Product, slug=product_slug)
            username = request.data.get('user')
            user = get_object_or_404(User, username=username)

            try:
                favorite_shop = FavoriteShop.objects.get(user=user, product=product)
            except FavoriteShop.DoesNotExist:
                # if the FavoriteShop object doesn't exist, return a response with status code 404
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            favorite_shop = get_object_or_404(FavoriteShop, pk=pk)

        favorite_shop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        user = request.user
        favorite_shops = FavoriteShop.objects.filter(user=user)
        serializer = self.serializer_class(favorite_shops, many=True)
        return Response(serializer.data)
    
class FavoriteShopView(APIView):
    
    def delete(self, request):
        print('call delete')
        print(request.data)
        # get the user and product from the request data
        product_slug = request.data.get('product')
        product = get_object_or_404(Product, slug=product_slug)
        username = request.data.get('user')
        user = get_object_or_404(User, username=username)

        # try to retrieve the FavoriteShop object using the user and product
        try:
            favorite_shop = FavoriteShop.objects.get(user=user, product=product)
        except FavoriteShop.DoesNotExist:
            # if the FavoriteShop object doesn't exist, return a response with status code 404
            return Response(status=status.HTTP_404_NOT_FOUND)

        # delete the FavoriteShop object and return a response with status code 204
        favorite_shop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_object(self, product_slug,username):
        print('call get object')
        product = get_object_or_404(Product, slug=product_slug)
        user = get_object_or_404(User, username=username)
        try:
            favorite_shop = FavoriteShop.objects.get(product=product, user=user)
            print(favorite_shop)
            return favorite_shop
        except FavoriteShop.DoesNotExist:
            raise NotFound("This shop has not been favorited.")
    
    def get(self, request, product_slug, username, format=None):
  
        try:
            favorite_shop = self.get_object(product_slug,username)
            serializer = FavoriteShopSerializer(favorite_shop)
            return Response(serializer.data)
        except NotFound as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)


