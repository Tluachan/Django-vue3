from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):     
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.slug}/'
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''
    
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail
    

    #To personalize what to be shown with plural form from this class
    class Meta:
        verbose_name_plural = 'Categories'

        

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=20, blank=True)
    map_url = models.URLField(blank=True)
    avg_rating = models.FloatField(blank=True, null=True)
    owner = models.ForeignKey(User, blank=True,null=True,on_delete=models.CASCADE)
    favorite_count= models.IntegerField(blank=True,null=True)

    class Meta:
        ordering = ('-avg_rating',)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''
    
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
    
    def get_rating(self):
        reviews = Review.objects.filter(product=self)
        if len(reviews) == 0:
            return 0
        total = 0
        for review in reviews:
            total += review.rating
        return total / len(reviews)
    
    def update_rating(self):
        self.avg_rating = self.get_rating()
        self.save()

    def update_favorite_count(self):
        self.favorite_count = FavoriteShop.objects.filter(product=self).count()
        self.save()
    

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.TextField(default='')
    rating = models.FloatField(default=0.0)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class FavoriteShop(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE,)
    product = models.ForeignKey(Product,blank=True,null=True,on_delete=models.CASCADE,)

    def __str__(self):
        return self.user.first_name + ":" + self.product.name