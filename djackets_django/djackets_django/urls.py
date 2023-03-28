from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include, re_path
from product.views import CategoryList
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    #django-vue
    path('api/v1/',include('djoser.urls')),
    path('api/v1/',include('djoser.urls.authtoken')),
    path('api/v1/',include('product.urls')),
    # Vue.js
    re_path("^.*$", TemplateView.as_view(template_name="index.html")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
