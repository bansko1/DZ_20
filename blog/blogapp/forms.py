from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Название')
    email = forms.EmailField(label='e-mail')
    message = forms.CharField(label='Сообщение')

class WordCreateForm(forms.Form):
    name = forms.CharField(label='Запрос')
    pages = forms.IntegerField(label='Количество анализируемых страниц ', initial=5)

class ReqForm(forms.Form):
    req = forms.CharField(label='Запрос ')
    sity = forms.CharField(label='Город (отбор вакансий) ')
    # pages = forms.IntegerField(label='Количество анализируемых страниц ', initial=5)