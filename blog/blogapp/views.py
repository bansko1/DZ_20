from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView, DetailView, CreateView, DeleteView
from django.shortcuts import render

from .models import Word_skill, Word, Vacancy, Area
from .forms import ContactForm, ReqForm, WordCreateForm
from blogapp.management.commands.fill_db import Command


# Create your views here.

class ContView(TemplateView):  # Класс для отображения контактрной информации
    template_name = 'blogapp/contact.html'


class WordListView(ListView):  # Класс для отображения списка запросов
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


class WordDetailView(DetailView):  # Класс для отображения детальной информации по одному запросу
    model = Word
    template_name = 'blogapp/word_detail.html'

    def get(self, request, *args, **kwargs):  # Метод обработки get запроса
        self.word_id = kwargs['pk']
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        '''
        Получение этого объекта
        :param queryset:
        :return:
        '''
        return get_object_or_404(Word, pk=self.word_id)


@login_required  # Только залогиненный
def word_skill(request, id):  # Функция для отображения навыков по конкретному запросу
    word = Word.objects.get(id=id)
    # skills = Word_skill.objects.filter(id_word=id).all()
    skills = Word_skill.objects.filter(id_word=id).select_related(
        'id_skill').all()  # Оптимизация запросов  в БД с помощью select_related
    return render(request, 'blogapp/word_skill.html', context={'word': word, 'skills': skills})


def word_area(request, id):  # Функция для отображения городов по конкретному запросу
    word = Word.objects.get(id=id)
    areas = Area.objects.filter(id_word=id).all()
    paginator = Paginator(areas, 10)

    page = request.GET.get('page')
    try:
        areas = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        areas = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        areas = paginator.page(paginator.num_pages)

    return render(request, 'blogapp/word_area.html', context={'word': word, 'areas': areas})


class WordCreateView(UserPassesTestMixin, FormView):  # Класс для создания поискового запроса (только суперпользователь)
    form_class = WordCreateForm
    model = Word
    success_url = reverse_lazy('blog:word_list')
    template_name = 'blogapp/word_create.html'

    def test_func(self):  # Класс для создания запроса
        return self.request.user.is_superuser  # только суперпользователь
        # return self.request.user.is_autor == True  # только автор

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        # Получаем данные из формы
        name = form.cleaned_data['name']
        pages = form.cleaned_data['pages']

        try:
            Word.objects.get(name=name)
        except ObjectDoesNotExist:
            com = Command(name, pages, self.request.user)  # Создаем запрос и заполняем по нему базу данных
            com.handle()
        return super().form_valid(form)


class WordDeleteView(UserPassesTestMixin, DeleteView):  # Класс для удаления запроса (только суперпользователь)
    template_name = 'blogapp/word_delete_confirm.html'
    model = Word
    success_url = reverse_lazy('blog:word_list')

    def test_func(self):  # Класс для создания запроса
        return self.request.user.is_superuser  # только суперпользователь


class ContactView(FormView):  # Класс для создания, заполнения и отображения формы для связи (любые пользователи)
    form_class = ContactForm
    # model = ContactForm
    success_url = reverse_lazy('blog:word_list')
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


class AreaListView(ListView):  # Класс для отображения списка городов (любые пользователи)
    model = Area
    template_name = 'blogapp/area_list.html'

    # context_object_name = 'areas'
    paginate_by = 15  # Вывод по 20 строк на страницу

    def get_queryset(self, **kwargs):
        return Area.objects.all().select_related('id_word')  # Оптимизация запросов  в БД с помощью select_related


@login_required  # Только залогиненный
def vac_create(request):  # Функция для заполнения формы и отбора вакансий по запросу и городу
    if request.method == 'POST':
        form = ReqForm(request.POST)
        if form.is_valid():
            req = form.cleaned_data['req']
            sity = form.cleaned_data['sity']
            try:
                v = Word.objects.get(name=req)  # Убрал дублирование запроса
            except ObjectDoesNotExist:
                return render(request, 'blogapp/word_text.html',
                              context={'req': req, 'text': 'Нет такого запроса. Создайте запрос.'})
            # v = Word.objects.get(name=req)      Убрал дублирование запросов
            a = Area.objects.get(name=sity, id_word=v)
            vac = Vacancy.objects.filter(word=v, area=a).all()

            return render(request, 'blogapp/about.html', context={'vac': vac, 'word': v, 'area': a})
        else:
            return render(request, 'blogapp/form.html', context={'form': form})
    else:
        form = ReqForm()
        return render(request, 'blogapp/form.html', context={'form': form})


def vac_word_area(request, id):  # Функция для отображения вакансий по городам и по конкретному запросу

    area = Area.objects.get(id=id)
    word = Word.objects.get(area=area)
    vacan = Vacancy.objects.filter(word=word, area=area).all()
    paginator = Paginator(vacan, 5)

    page = request.GET.get('page')
    try:
        vacan = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        vacan = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        vacan = paginator.page(paginator.num_pages)

    return render(request, 'blogapp/vac_list.html', context={'word': word, 'area': area, 'vacan': vacan})
