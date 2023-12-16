from django import forms
from .models import Word, Area


class ContactForm(forms.Form):
    name = forms.CharField(label='Название')
    email = forms.EmailField(label='e-mail')
    message = forms.CharField(label='Сообщение')


class WordCreateForm(forms.Form):
    name = forms.CharField(label='Запрос')
    pages = forms.IntegerField(label='Количество анализируемых страниц ', initial=2)

    class Meta:
        model = Word
        # fields = '__all__'
        exclude = ('count', 'user')

class SearchAreaForm(forms.Form):
    name = forms.CharField(label='Поиск города', widget=forms.TextInput(attrs={'placeholder':'Название'}))
    class Meta:
        model = Area
        exclude = ('id_word',)

class ReqForm(forms.Form):
    req = forms.CharField(label='Запрос ')
    sity = forms.CharField(label='Город (отбор вакансий) ')
