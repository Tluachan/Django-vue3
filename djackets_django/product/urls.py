from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product import views
from .views import ReviewViewSet, FavoriteShopViewSet

#router = DefaultRouter()
#router.register('favorite-shops', FavoriteShopViewSet, basename='favorite-shops')

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('products/search/',views.search),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('products/<slug:category_slug>/',views.CategoryDetail.as_view()),
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('products/<slug:product_slug>/reviews', views.ReviewList.as_view()),
    path('reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='review-list'),
    path('reviews/<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='review-detail'),
    path('favorite-shops/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='review-list'),
    path('favorite-shops/<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='review-detail'),
]


