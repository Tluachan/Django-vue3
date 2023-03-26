from django.urls import path, include
from rest_framework.routers import DefaultRouter

from product import views
from .views import ReviewViewSet, FavoriteShopViewSet, FavoriteShopView, UserAllReviewList, ProductViewSet, SortedProductList

#router = DefaultRouter()
#router.register('favorite-shops', FavoriteShopViewSet, basename='favorite-shops')

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('products/search/',views.search),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view()),
    path('products/create/',ProductViewSet.as_view({'post': 'create'})),
    path('products/getlist/',ProductViewSet.as_view({'get': 'list'})),
    path('products/<int:pk>/', ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='delete_product'),
    path('products/<slug:category_slug>/',views.CategoryDetail.as_view()),
    path('categories/', views.CategoryList.as_view(), name='category_list'),
    path('products/<slug:category_slug>/product-list',views.SortedProductList.as_view()),
    path('products/<slug:product_slug>/reviews', views.ReviewList.as_view()),
    path('reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='review-list'),
    path('reviews/<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='review-detail'),
    path('favorite-shops/', FavoriteShopViewSet.as_view({'get': 'list', 'post': 'create'}), name='favorite-list'),
    #path('favorite-shops/<int:pk>/', FavoriteShopViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='favorite-detail'),
    path('favorite-shops/delete/', FavoriteShopView.as_view(), name='favorite-shop-delete'),
    path('favorite-shops/product/<slug:product_slug>/user/<slug:username>/', FavoriteShopView.as_view(), name='favorite-shop-get'),
    path('reviews/user/<slug:username>/', UserAllReviewList.as_view(), name='user_review_list'),
]


