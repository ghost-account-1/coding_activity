from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from app.models import MyUser

class MyUserTests(APITestCase):
    def test_create_account_and_token_and_is_not_active(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('users-list')
        data = {'email': 'DabApps@example.com', 'password': 'password', 'first_name': '', 'last_name': '',}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        token = Token.objects.get(user__email='DabApps@example.com')
        self.assertEqual(MyUser.objects.count(), 1)
        self.assertEqual(MyUser.objects.get().email, 'DabApps@example.com')
        self.assertTrue(token)
        self.assertFalse(MyUser.objects.get().is_active)

    #def test_user_activation(self):
    #    url = reverse('users-list')
    #    data = {'email': 'DabApps@example.com', 'password': 'password', 'first_name': '', 'last_name': '',}

    #    response = self.client.post(url, data, format='json')
    #    token = Token.objects.get(user__email='DabApps@example.com')
    #    user = MyUser.objects.get()

    #    detail_url = '127.0.0.1:8000' + url + str(user.id) + '/'

    #    self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    #    print((detail_url))
    #    print((url))
    #    activate = self.client.post(detail_url, {}, format='json')
    #    print (activate)
    #    print(user.email)

    #    self.assertTrue(MyUser.objects.get().is_active)
