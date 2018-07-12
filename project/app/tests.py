from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APITransactionTestCase
from rest_framework.authtoken.models import Token
from app.models import MyUser
from app.views import login, MyUserViewSet
import requests
from rest_framework.test import APIRequestFactory
from requests.auth import HTTPBasicAuth
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory

class MyUserTests(APITestCase):
    def test_create_account_and_token_and_is_not_active(self):
        """
        Ensure we can create a new account object.
        """
        create_url = reverse('users-list')
        create_data = {'email': 'test_data@example.com', 'password': 'password', 'first_name': 'first_name', 'last_name': 'last_name',}
        create_response = self.client.post(create_url, create_data, format='json')
        token = Token.objects.get(user__email='test_data@example.com')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MyUser.objects.count(), 1)
        self.assertEqual(token.user.email, 'test_data@example.com')
        self.assertTrue(token)
        self.assertFalse(token.user.is_active)

    def test_user_activation(self):
        create_url = reverse('users-list')
        create_data = {'email': 'test_data@example.com', 'password': 'password', 'first_name': 'first_name', 'last_name': 'last_name',}
        create_response = self.client.post(create_url, create_data, format='json')
        token = Token.objects.get(user__email='test_data@example.com')

        activate_user = '/api/activation/'
        activate_data = {}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        activate_response = self.client.patch(activate_user, activate_data, format='json')
        self.assertEqual(activate_response.status_code, 202)
        self.assertTrue(MyUser.objects.get(id=activate_response.data['id']).is_active)


    def test_list_users_no_oauth(self):
        create_url = reverse('users-list')
        create_data = {'email': 'test_data@example.com', 'password': 'password', 'first_name': 'first_name', 'last_name': 'last_name',}
        create_response = self.client.post(create_url, create_data, format='json')
        token = Token.objects.get(user__email='test_data@example.com')

        token.user.is_active = True
        token.user.save()


        list_users = '/api/users/'
        list_data = {}
        list_response = self.client.get(list_users, list_data, format='json')
        self.assertEqual(list_response.data[0].get('id'), token.user.id)
        self.assertEqual(list_response.data[0].get('first_name'), create_data['first_name'])
        self.assertEqual(list_response.data[0].get('email'), None)
        self.assertEqual(list_response.data[0].get('last_name'), None)

    def test_list_users_with_oauth(self):
        create_url = reverse('users-list')
        create_data = {'email': 'test_data@example.com', 'password': 'password', 'first_name': 'first_name', 'last_name': 'last_name',}
        create_response = self.client.post(create_url, create_data, format='json')
        token = Token.objects.get(user__email='test_data@example.com')

        list_users = '/api/users/'
        list_data = {}
        self.client.force_authenticate(user=token.user)
        list_response = self.client.get(list_users, list_data, format='json')

        self.assertEqual(list_response.data[0].get('first_name'), create_data['first_name'])
        self.assertEqual(list_response.data[0].get('email'), create_data['email'])
        self.assertEqual(list_response.data[0].get('last_name'), create_data['last_name'])

    def test_change_password_wrong_password(self):
        create_url = reverse('users-list')
        create_data = {'email': 'test_data@example.com', 'password': 'password', 'first_name': 'first_name', 'last_name': 'last_name',}
        create_response = self.client.post(create_url, create_data, format='json')
        token = Token.objects.get(user__email='test_data@example.com')

        self.client.force_authenticate(user=token.user)
        change_password = '/api/password/'
        change_data = {"old_password":"password","new_password":"password"}
        change_response = self.client.put(change_password, change_data, format='json')
        self.assertEqual(change_response.status_code, 401)

    #def test_login_user(self):
#        create_url = reverse('users-list')
#        create_data = {'email': 'test_data@example.com', 'password': 'password', 'first_name': '', 'last_name': '',}
#        create_response = self.client.post(create_url, create_data, format='json')
#        token = Token.objects.get(user__email='test_data@example.com')
#        token.user.is_active = True
#        token.user.save()
#        #token.user.refresh_from_db()
#
#        #activate_user = MyUser.objects.get(id=create_response.data['id'])
#        #activate_user.is_active = True
#        #activate_user.save()
#
#        #login_data = "grant_type=password&username=" + create_data['email'] + "&password=" + create_data['password']
#        #headers = {"content-type": "application/x-www-form-urlencoded"}
#        #r_ = requests.post('http://localhost:8000/o/token/', data=data, auth=(CLIENT_ID, CLIENT_SECRET), headers=headers)
#
#
#        login_user = '/o/token/'
#        #list_user = '/api/users/'
#        factory = APIRequestFactory()
#        request = factory.post(login_user, {'email': create_data['email'], 'password': create_data['password']})
#
#        #self.client.auth = HTTPBasicAuth(create_data['email'], create_data['password'])
#        #login_response = self.client.post(login_user, login_data, format='json')
#        #import pprint;pprint.pprint(vars(login_response))
#        #login_response = self.client.post(list_user, login_data, format='json', HTTP_AUTHORIZATION='Bearer ' + token.key)
#
#        import pdb;pdb.set_trace()


