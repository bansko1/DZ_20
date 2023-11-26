from django import forms
from .models import Word


class ContactForm(forms.Form):
    name = forms.CharField(max_length=32, label='От кого')
    email = forms.EmailField(label='e-mail')
    message = forms.CharField(label='Ваше сообщение')


class WordCreateForm(forms.Form):
    name = forms.CharField(max_length=56, label='Запрос')
    pages = forms.IntegerField(label='Количество анализируемых страниц ', initial=2)

    class Meta:
        model = Word
        # fields = '__all__'
        exclude = ('count', 'user')


class ReqForm(forms.Form):
    req = forms.CharField(label='Запрос ')
    sity = forms.CharField(label='Город (отбор вакансий) ')
