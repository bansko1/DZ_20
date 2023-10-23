from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView, DetailView, CreateView, DeleteView
from django.shortcuts import render

from .models import Word_skill, Word, Vacancy, Area
from .forms import ContactForm, ReqForm
from blogapp.management.commands.fill_db import Command


# Create your views here.

class ContView(TemplateView):                    # Класс для отображения контактрной информации
    template_name = 'blogapp/contact.html'

class VacancyListView(ListView):                        # Класс для отображения вакансий
    model = Vacancy
    template_name = 'blogapp/vacancy_list.html'
    queryset = Vacancy.objects.filter(word=27, area=80)

class WordListView(ListView):                           # Класс для отображения списка запросов
    model = Word
    template_name = 'blogapp/word_list.html'
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['name'] = 'Запросы'
        return context

    def get_queryset(self):
        list_all = Word.objects.all()
        # list_ = list_all[2:]
        return list_all

class WordDetailView(DetailView):                       # Класс для отображения одного запроса
    model = Word
    template_name = 'blogapp/word_detail.html'
    def get(self, request, *args, **kwargs):            # Метод обработки get запроса
        self.word_id = kwargs['pk']
        return super().get(request, *args, **kwargs)
    def get_object(self, queryset=None):
        '''
        Получение этого объекта
        :param queryset:
        :return:
        '''
        return get_object_or_404(Word, pk=self.word_id)

class WordCreateView(CreateView):                       # Класс для создания запроса
    fields = '__all__'
    model = Word
    success_url = reverse_lazy('blog:word_list')
    template_name = 'blogapp/word_create.html'

class WordDeleteView(DeleteView):
    template_name = 'blogapp/word_delete_confirm.html'
    model = Word
    success_url = reverse_lazy('blog:word_list')



class WsListView(ListView):                         # Класс для отображения навыков по запросам
    model = Word_skill
    template_name = 'blogapp/ws_list.html'
    queryset = Word_skill.objects.filter(id_word=26)
    # def get(self, request, *args, **kwargs):
    #     self.id_word = kwargs['pk']
    #     return super().get(request, *args, **kwargs)

class ContactView(FormView):                        # Класс для создания, заполнения и отображения формы для связи
        form_class = ContactForm
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

class AreaListView(ListView):
    model = Area
    template_name = 'blogapp/area_list.html'

def word_create(request):
    if request.method == 'POST':
        form = ReqForm(request.POST)
        if form.is_valid():
            req = form.cleaned_data['req']
            pages = form.cleaned_data['pages']
            sity = form.cleaned_data['sity']
            # print(req, pages, sep='\n')
            try:
                Word.objects.get(name=req)
            except ObjectDoesNotExist:
                com = Command(req, pages)
                com.handle()
            v = Word.objects.get(name=req)
            a = Area.objects.get(name=sity)
            s = Word_skill.objects.filter(id_word=v.id).all()
            vac = Vacancy.objects.filter(word=v, area=a).all()
            # print(vac, v, s, sep='\n')
            return render(request, 'blogapp/about.html', context={'vac': vac, 'word': v, 'skills': s, 'area': a})
        else:
            return render(request, 'blogapp/form.html', context={'form': form})
    else:
        form = ReqForm()
        return render(request, 'blogapp/form.html', context={'form': form})

# def result(request):
#     if request.method == 'POST':
#         form = ReqForm(request.POST)
#         if form.is_valid():
#             vac = form.cleaned_data['vacancy']
#             pages = form.cleaned_data['pages']
#             print(vac, pages, sep='\n')
#             # com = Command(vac, pages, where)
#             # com.handle()
#             v = Word.objects.get(name=vac)
#             s = Word_skill.objects.filter(id_word=v.id).all()
#             vac = Vacancy.objects.filter(word=v).all()
#             print(vac, v, s, sep='\n')
#             return render(request, 'blogapp/about.html', context={'vac': vac, 'word': v, 'skills': s})
#         else:
#             # form1 = ReqForm
#             return render(request, 'blogapp/form.html', context={'form': form})