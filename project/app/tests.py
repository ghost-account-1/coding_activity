from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from app.models import MyUser
import requests
from rest_framework.test import APIRequestFactory

class MyUserTests(APITestCase):
    def test_create_account_and_token_and_is_not_active(self):
        """
        Ensure we can create a new account object.
        """
        create_url = reverse('users-list')
        create_data = {'email': 'test_data@example.com', 'password': 'password', 'first_name': '', 'last_name': '',}
        create_response = self.client.post(create_url, create_data, format='json')
        token = Token.objects.get(user__email='test_data@example.com')
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MyUser.objects.count(), 1)
        self.assertEqual(MyUser.objects.get().email, 'test_data@example.com')
        self.assertTrue(token)
        self.assertFalse(MyUser.objects.get().is_active)

    def test_user_activation(self):
        create_user = reverse('users-list')
        create_data = {'email': 'test_data@example.com', 'password': 'password', 'first_name': '', 'last_name': '',}
        create_response = self.client.post(create_user, create_data, format='json')
        token = Token.objects.get(user__email='test_data@example.com')

        activate_user = '/api/activation/'
        activate_data = {}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        activate_response = self.client.patch(activate_user, activate_data, format='json')
        self.assertEqual(activate_response.status_code, 202)
        self.assertTrue(MyUser.objects.get(id=activate_response.data['id']).is_active)



    def test_login_user(self):
        create_user = reverse('users-list')
        create_data = {'email': 'test_data@example.com', 'password': 'password', 'first_name': '', 'last_name': '',}
        create_response = self.client.post(create_user, create_data, format='json')
        token = Token.objects.get(user__email='test_data@example.com')

        #activate_user = MyUser.objects.get(id=create_response.data['id'])
        #activate_user.is_active = True
        #activate_user.save()

        login_user = '/api/login/'
        login_response = self.client.post(login_user, create_data, format='json')
        #import pdb;pdb.set_trace()

