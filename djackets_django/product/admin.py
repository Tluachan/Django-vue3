from django.contrib import admin

from .models import Category, Product, Review, FavoriteShop

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    list_display = ('name','category','avg_rating')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'product', 'rating')

class FavoriteShopAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'product')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(FavoriteShop, FavoriteShopAdmin)