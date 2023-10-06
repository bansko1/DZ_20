from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse

from .models import Word_skill
from .forms import ContactForm

# Create your views here.

def main_view(request):
    w_s = Word_skill.objects.all()
    return render(request, 'blogapp/index.html', context={'w_s': w_s})

def create_post(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Получаем данные из формы
            name = form.cleaned_data['name']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            send_mail(
                'Contact message',
                f'Ваше сообщение {message} принято',
                'test@test.ru',
                [email],
                fail_silently=True
            )
            return HttpResponseRedirect(reverse('blog:index'))
        else:
            return render(request, 'blogapp/create.html', context={'form': form})
    else:
        form = ContactForm()
        return render(request, 'blogapp/create.html', context={'form':form})

# def post(request, id):
#     post = get_object_or_404(Post, id=id)

def contact(request):
    return render(request, 'blogapp/contact.html')
