from random import randint

from django.test import TestCase
from .models import Word
from userapp.models import BlogUser
# faker - генерирует простые данные, например имя
from faker import Faker
# FactoryBoy - генерирует данные для конкретной модели django
# mixer - полностью создать fake модель
from mixer.backend.django import mixer


# Create your tests here.
# class WordTestCase(TestCase):
#
#     def setUp(self):
#         user = BlogUser.objects.create_user(username='test_name',
#                                             email='test@test.com', password='testtest123456', is_autor=True)
#         self.word = Word.objects.create(name='test_word', count=3000, user=user)
#
#         self.word_str = Word.objects.create(name='test_word_str', count=2000, user=user)
#
#     def test_what_count(self):
#         self.assertTrue(self.word.what_count())
#
#     def test_some_metod(self):
#         self.assertEqual(self.word.some_metod(), 'Привет из метода some_metod !', msg='Не эквивалентно')
#
#     def test_str(self):
#         self.assertEqual(str(self.word_str), 'test_word_str')
#
#
# class WordTestCaseFaker(TestCase):
#
#     def setUp(self):
#         faker = Faker()
#         user = BlogUser.objects.create_user(username=faker.name(),
#                                             email='test@test.com', password='testtest123456', is_autor=True)
#         self.word = Word.objects.create(name=faker.name(), count=3000, user=user)
#         print(user.username)
#         print(self.word.name)
#
#         self.word_str = Word.objects.create(name='test_word_str', count=2000, user=user)
#
#     def test_what_count(self):
#         self.assertTrue(self.word.what_count())
#
#     def test_some_metod(self):
#         self.assertEqual(self.word.some_metod(), 'Привет из метода some_metod !', msg='Не эквивалентно')
#
#     def test_str(self):
#         self.assertEqual(str(self.word_str), 'test_word_str')


class WordTestCaseMixer(TestCase):

    def setUp(self):
        self.word = mixer.blend(Word, count=randint(1, 500) + 1000)
        print('mixer name: ', self.word.name)
        print('mixer user: ', self.word.user)
        print('mixer count: ', self.word.count)
        # print('mixer user name: ', self.word.user.username)
        print('mixer user email: ', self.word.user.email)

        self.word_str = mixer.blend(Word, name='test_word_str', count=randint(1, 500) + 1000)
        print('mixer name_: ', self.word_str.name)
        print('mixer count_: ', self.word_str.count)

    def test_what_count(self):
        self.assertTrue(self.word.what_count())

    def test_some_metod(self):
        self.assertEqual(self.word.some_metod(), 'Привет из метода some_metod !', msg='Не эквивалентно')

    def test_str(self):
        self.assertEqual(str(self.word_str), 'test_word_str')
