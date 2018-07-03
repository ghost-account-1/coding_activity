from rest_framework import routers, serializers, viewsets
from app.models import MyUser

class MyUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'email', 'password', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Creates and saves a User with the given email
        and password.
        """

        if not validated_data['email']:
            raise ValueError('Users must have an email address')

        user = MyUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MyUserViewset(viewsets.ModelViewSet):
    query = MyUser.objects.all()
    serializer_class = MyUserSerializer

