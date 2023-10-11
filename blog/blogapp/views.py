from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView

from .models import Word_skill, Word
from .forms import ContactForm


# Create your views here.

class ContView(TemplateView):
    template_name = 'blogapp/contact.html'

class WordListView(ListView):
    model = Word
    template_name = 'blogapp/word_list.html'

class WsListView(ListView):
    model = Word_skill
    template_name = 'blogapp/ws_list.html'

class ContactView(FormView):
        form_class = ContactForm
        # fields = '__all__'
        model = ContactForm
        success_url = reverse_lazy('blog:ws_list')
        template_name = 'blogapp/form_create.html'

        def form_valid(self, form):
            # This method is called when valid form data has been POSTed.
            # It should return an HttpResponse.
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
            return super().form_valid(form)
