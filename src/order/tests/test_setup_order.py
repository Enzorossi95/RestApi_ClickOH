from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker
# Create your tests here.


"""
Modulo para realizar el login y obtener token en los test.
"""


class TestOrderSetUp(APITestCase):

    def setUp(self):
        from django.contrib.auth.models import User
        faker = Faker()

        self.login_url = '/dj-rest-auth/login/'
        self.user = User.objects.create_superuser(
            username=faker.name(),
            password='developer',
            email=faker.email()
        )

        response = self.client.post(
            self.login_url,
            {
                'username': self.user.username,
                'password': 'developer'
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #import pdb; pdb.set_trace()
        self.token = response.data['key']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        return super().setUp()
