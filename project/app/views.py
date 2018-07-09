import ast
from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model
from rest_framework import viewsets, status, mixins
from app.models import MyUser
from app.serializers import MyUserSerializer, UserListSerializer
from rest_framework.response import Response
from rest_framework import permissions, authentication, exceptions
from rest_framework.decorators import action, api_view, authentication_classes
from rest_framework.authtoken.models import Token
from project.settings import CLIENT_ID, CLIENT_SECRET
from django.urls import reverse
import oauth2_provider.urls
import requests
from requests.auth import HTTPBasicAuth
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope, TokenMatchesOASRequirements, IsAuthenticatedOrTokenHasScope
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from datetime import datetime, timedelta
import pytz


class ActivationAuthentication(authentication.TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except:
            return super(ActivationAuthentication, self).authenticate_credentials(key)
        print(key)
        myuser = MyUser.objects.get(email=token.user.email)
        print(myuser)

        if token:
            myuser = MyUser.objects.get(email=token.user.email)
            myuser.is_active = True
            myuser.save()

        return (token.user, token)

class LoginAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            email = request.data['email']
            password = request.data['password']
        except:
            raise exceptions.AuthenticationFailed(("email and password fields are required"))

        if not email or not password:
            raise exceptions.AuthenticationFailed(('No credentials provided.'))
        credentials = {
            get_user_model().USERNAME_FIELD: email,
            'password': password
        }

        user = authenticate(**credentials)
        if user is None:
            raise exceptions.AuthenticationFailed(('Invalid username/password. Or the user is inactive.'))
        return (user, None)

class ActivationViewSet(generics.UpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    authentication_classes = (ActivationAuthentication,)

    def partial_update(self, request, pk=None):
        try:
            myuser = MyUser.objects.get(pk=request.user.id)
            response = {"id":myuser.id,
                    "email":myuser.email,
                    "first_name":myuser.first_name,
                    "last_name":myuser.last_name}
            return Response(response)
        except:
            return Response({'detail': 'You need an activation token. Check your email.'})

class ChangePasswordViewSet(generics.UpdateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    authentication_classes = (OAuth2Authentication,)

    def update(self, request, pk=None):
        try:
            old_password = request.data['old_password']
            new_password = request.data['new_password']
        except:
            return Response({"email":["This field is required."],"password":["This field is required."]})
        if request.user and request.user.is_authenticated:
            if authenticate(email=request.user.email, password=old_password):
                request.user.set_password(request.data['new_password'])
                request.user.save()
                return Response({'detail': 'Password changed'})
            return Response({'detail': 'User must have a wrong password'})
        if request.oauth2_error:
            return Response(request.oauth2_error)
        return Response({'detail': 'User is not Authenticated'})

class MyUserViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer

    def list(self, request):
        serializer_class = UserListSerializer
        authentication_classes = (OAuth2Authentication,)
        if request.user and request.user.is_authenticated:
            serializer = MyUserSerializer(self.queryset, many=True)
            return Response(serializer.data)
        serializer = serializer_class(self.queryset, many=True)
        if request.oauth2_error:
            return Response(request.oauth2_error)
        return Response(serializer.data)


@api_view(['POST'])
@authentication_classes((LoginAuthentication,))
def login(request, format=None):
    email = request.data['email']
    password = request.data['password']

    data = "grant_type=password&username=" + email + "&password=" + password
    headers = {"content-type": "application/x-www-form-urlencoded"}
    r_ = requests.post('http://localhost:8000/o/token/', data=data, auth=(CLIENT_ID, CLIENT_SECRET), headers=headers)
    content = ast.literal_eval(r_.content.decode("utf-8"))
    try:
        response = {"access_token": content['access_token'],
                    "token_type": content['token_type'],
                    "scope": content['scope'],
                    "refresh_token": content['refresh_token'],
                    "expires_in": content['expires_in']}
    except:
        return Response(content, status=r_.status_code)
    return Response(response, status=r_.status_code)
