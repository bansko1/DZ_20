from django.urls import path, include
from .models import Word, Skill, Vacancy, Area
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class SkillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skill
        # fields = ['name']
        fields = '__all__'
class WordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Word
        fields = ['url', 'name', 'count']

class AreaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Area
        # fields = ['name']
        fields = '__all__'

class VacancySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Vacancy
        fields = '__all__'