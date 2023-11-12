from django.test import TestCase, Client
from faker import Faker

from userapp.models import BlogUser


class OpenViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.fake = Faker()

    def test_statuses(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/form-create/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/form-create/',
                                    {'name': self.fake.name(), 'message': self.fake.text(), 'email': self.fake.email()})
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/')
        self.assertTrue('name' in response.context)

    def test_login_required(self):
        BlogUser.objects.create_user(username='test_name',
                                     email='test@test.com', password='testtest123456', is_autor=True)
        response = self.client.get('/form/')
        self.assertEqual(response.status_code, 302)  # Проверка статуса ответа на запрос незалогиненного пользователя

        self.client.login(username='test_name', password='testtest123456')
        response = self.client.get('/form/')
        self.assertEqual(response.status_code, 200)  # Проверка статуса ответа на запрос залогиненного пользователя

        self.client.logout()
        response = self.client.get('/word-create/')
        self.assertEqual(response.status_code, 302)  # Проверка статуса ответа на запрос незалогиненного пользователя

        self.client.login(username='alex', password='alexalexalex')
        response = self.client.get('/word-create/')
        self.assertEqual(response.status_code, 302)  # Проверка статуса ответа на запрос суперпользователя

        self.client.login(username='test_name', password='testtest123456', is_autor=False)
        response = self.client.get('/word-create/')
        self.assertEqual(response.status_code,
                         403)  # Проверка статуса ответа на запрос залогиненного, но не суперпользователя