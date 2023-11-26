from .models import Skill, Word, Vacancy, Area
from .serializers import SkillSerializer, WordSerializer, VacancySerializer, AreaSerializer
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import ReadOnly, IsAutor
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication

class SkillViewSet(viewsets.ModelViewSet):       # Права на чтение для всех, редактирование для авторизованных
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class WordlViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser|ReadOnly]     # Права на чтение для всех, на редактирование для админа
    queryset = Word.objects.all()
    serializer_class = WordSerializer

class AreaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser|IsAutor|ReadOnly]  # Права на чтение для всех, редактирование для автора и админа
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

class VacancylViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication, SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser|IsAutor]  # Права на чтение, редактирование для автора и админа
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer