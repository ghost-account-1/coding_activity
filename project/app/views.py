from django.shortcuts import render
from rest_framework import viewsets, status, mixins
from app.models import MyUser
from app.serializers import MyUserSerializer
from rest_framework.response import Response
from rest_framework import permissions, authentication
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token

class CustomPermission(permissions.BasePermission):
    """
    Global permission check for blacklisted IPs.
    """

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

class MyUserViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin):
    """
    Example empty viewset demonstrating the standard
    actions that will be handled by a router class.

    If you're using format suffixes, make sure to also include
    the `format=None` keyword argument for each action.
    """
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer
    authentication_classes = (CustomAuthentication,)

    def list(self, request):
        queryset = MyUser.objects.all()
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        #print(request.user.token)
        #print(MyUser.objects.filter(request.user))
        #print(request.auth)
        #import pdb;pdb.set_trace()
        #if CustomAuthentication:
        #    print('Authenticated')
        #else:
        #    print('Not Authenticated')
        return super(MyUserViewSet, self).retrieve(request, *args, **kwargs)

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'retrieve':
            permission_classes = [CustomPermission]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
