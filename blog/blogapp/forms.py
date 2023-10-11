from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Название')
    email = forms.EmailField(label='e-mail')
    message = forms.CharField(label='Сообщение')

# class PostForm(forms.ModelForm):
#     class Meta:
#         model = ContactForm
#         fields = '__all__'