from django.db import models

# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=16, unique=True)
    # count = models.IntegerField(blank=True)
    def __str__(self):
        return self.name

class Area(models.Model):                                   # Модель Города
    name = models.CharField(max_length=16, unique=True)
    def __str__(self):
        return self.name

class Word(models.Model):                                   # Модель Запросы
    name = models.CharField(max_length=32, unique=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'

class Vacancy(models.Model):                                # Модель Вакансии
    name = models.CharField(max_length=50)
    salary_from = models.IntegerField(default=0)
    salary_to = models.IntegerField(default=0)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.name} - {self.area} от {self.salary_from} до {self.salary_to}'

class Word_skill(models.Model):                              # Модель Навыки
    id_word = models.ForeignKey(Word, on_delete=models.CASCADE)
    id_skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    count = models.FloatField()
    percent = models.FloatField()
    def __str__(self):
        return f'{self.id_word} {self.id_skill} count={self.count}'