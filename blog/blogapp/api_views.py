from .models import Skill, Word
from .serializers import SkillSerializer, WordSerializer
from rest_framework import viewsets

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class WordlViewSet(viewsets.ModelViewSet):
    queryset = Word.objects.all()
    serializer_class = WordSerializer