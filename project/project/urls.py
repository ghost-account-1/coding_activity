"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from app import views
from app import serializers


router = routers.DefaultRouter()
router.register(r'users', views.MyUserViewSet, 'users')
admin.autodiscover()


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='app')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'api/login/$', views.login),
    url(r'api/activation/$', views.ActivationViewSet.as_view()),
    url(r'api/password/$', views.ChangePasswordViewSet.as_view()),


]
