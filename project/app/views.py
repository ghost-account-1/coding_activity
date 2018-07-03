from django.shortcuts import render
from rest_framework import viewsets
from app.models import MyUser
from app.serializers import MyUserSerializer


class MyUserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

