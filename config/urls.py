"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('livraria/', views.livraria, name='livraria'),
    path('cafeteria/', views.cafeteria, name='cafeteria'),
    path('sobre/', views.sobre, name='sobre'),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
