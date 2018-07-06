import ast
from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model
from rest_framework import viewsets, status, mixins
from app.models import MyUser
from app.serializers import MyUserSerializer
from rest_framework.response import Response
from rest_framework import permissions, authentication, exceptions
from rest_framework.decorators import action, api_view, authentication_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import BasicAuthentication
from project.settings import CLIENT_ID, CLIENT_SECRET
from django.urls import reverse
import oauth2_provider.urls
import requests
from requests.auth import HTTPBasicAuth

class CustomPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['GET']:
            object_id = obj.id
            object_token = Token.objects.get(user=obj.id) 

            request_id = request.user.id
            request_token = request.auth

            id_matched = request_id == object_id
            token_matched = request_token == object_token

            # activate if user and token matched
            if object_id == request_id and object_token == request_token:
                obj.is_active = True
                obj.save()
                return True
            else:
                return False
        else:
            return False

class CustomAuthentication(authentication.TokenAuthentication):
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
            if not token.user.is_active:
                print ('is not active')
                pass
            return (token.user, token)
        except:
            return super(CustomAuthentication, self).authenticate_credentials(key)

class LoginAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        email = request.data['email_address']
        password = request.data['password']

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



class MyUserViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    authentication_classes = (CustomAuthentication,)

    def list(self, request):
        queryset = MyUser.objects.all()
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        return super(MyUserViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = [CustomPermission]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

@api_view(['POST'])
@authentication_classes((LoginAuthentication,))
def login(request, format=None):
    email = request.data['email_address']
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
