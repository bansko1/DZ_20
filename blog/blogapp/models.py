from django.db import models
from userapp.models import BlogUser


# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name


class Word(models.Model):  # Модель Запросы
    name = models.CharField(max_length=56, unique=True)
    count = models.IntegerField(default=0)
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'

    def what_count(self):
        return bool(self.count > 1000)

    def some_metod(self):
        return 'Привет из метода some_metod !'


class Area(models.Model):  # Модель Города
    name = models.CharField(max_length=16)
    id_word = models.ForeignKey(Word, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.id_word}'


class Vacancy(models.Model):  # Модель Вакансии
    name = models.CharField(max_length=50)
    salary_from = models.IntegerField(default=0)
    salary_to = models.IntegerField(default=0)
    url = models.URLField()  # Добавление ссылки на вакансию
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.area} от {self.salary_from} до {self.salary_to}'


class Word_skill(models.Model):  # Модель Навыки
    id_word = models.ForeignKey(Word, on_delete=models.CASCADE)
    id_skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    count = models.FloatField()
    percent = models.FloatField()

    def __str__(self):
        return f'{self.id_word} {self.id_skill} count={self.count}'
