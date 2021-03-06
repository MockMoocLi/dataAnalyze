"""dataAnalyze URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from taobao.views import *


# router = DefaultRouter()
# router.register('index-api', index)

urlpatterns = [
    path('', include('taobao.urls')),
    path('admin/', admin.site.urls),
    # path('index-api/', include(router.urls)),
    path('index3', index3, name='index3'),
    # 网购
    path('onlineshop', onlineshop, name='onlineshop'),
    path('search_reslut', search_reslut, name='search_reslut'),
    # 酒店
    path('hotel', hotel, name='hotel'),
    path('hotel_reslut', hotel_reslut, name='hotel_reslut'),
    # 旅游
    path('travel', travel, name='travel'),
    path('travel_reslut', travel_reslut, name='travel_reslut'),
    # 美食
    path('cate', cate, name='cate'),
    path('cate_reslut', cate_reslut, name='cate_reslut'),
    # 导航
    path('map', map, name='map'),
    path('navigation', navigation, name='navigation'),
    # 食物相克
    path('food', food, name='food'),
    path('checkfood', checkfood, name='checkfood'),
]+static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
