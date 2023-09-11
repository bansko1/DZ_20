from django.core.management.base import BaseCommand
from blogapp.models import Post, Skill, Area
import requests


class Command(BaseCommand):
    def handle(self, *args, **options):

        text_vacancies = 'js developer'  # Название вакансии

        url_vacancies = 'https://api.hh.ru/vacancies'
        params = {
            'text': text_vacancies,
            'page': 1,
            'per_page': 20,
            'area': 113  # 113 - Россия
        }
        result = requests.get(url_vacancies, params=params).json()
        found = result['found']
        pages = result['pages']
        per_page = result['per_page']
        print('*****************************************')
        # print('Отбор вакансий по запросу: ', text_vacancies)
        # print('Всего найдено вакансий: ', found)
        # print(f'Всего страниц: {pages}, Вакансий на странице: {per_page}')
        # pprint.pprint(result)
        p = 0
        print('Вакансия ', p)
        item_one_vacancy = result['items'][p]
        one_vacancy_url = item_one_vacancy['url']
        result_one_vac = requests.get(one_vacancy_url).json()
        key_skills = result_one_vac['key_skills']                   # словарь ключевых навыков в вакансии
        # salary = result_one_vac['salary']                         # словарь с данными по зарплате
        sity = result_one_vac['area']                               # словарь с названием города
        # print('город ', sity['name'])
        # print(key_skills)
        # print(Skill.objects.all())
        # ****************************************
        Post.objects.create(name=text_vacancies)  # создаем query set объектов (таблицу) с вакансиями
        post = Post.objects.get(name=text_vacancies)  # получаем конкретную вакансии
        for item in key_skills:
            Skill.objects.create(name=item['name'], count=1)        # создаем query set объектов навыков
        skill = Skill.objects.all()  # получаем все навыки
        # post.skill.set(skill)                                     # определяем навыки конкретной вакансии
        Area.objects.create(name=sity['name'])                      # создаем query set объектов городов
        area = Area.objects.all()                                   # получаем все города
        # post.area.set(area)                                       # определяем города конкретной вакансии
        # ****************************************
        for p in range(1, 20):
            print('Вакансия ', p)
            item_one_vacancy = result['items'][p]
            one_vacancy_url = item_one_vacancy['url']
            result_one_vac = requests.get(one_vacancy_url).json()
            key_skills = result_one_vac['key_skills']               # словарь ключевых навыков в вакансии
            # salary = result_one_vac['salary']                     # словарь с данными по зарплате
            sity = result_one_vac['area']                           # словарь с названием города
            # ****************************************
            list_sities = []
            sities = Area.objects.all()
            for item in sities:
                list_sities.append(item.name)
            if sity['name'] not in list_sities:
                Area.objects.create(name=sity['name'])

            list_skills = []
            # count = 1
            skills = Skill.objects.all()
            for item in skills:
                list_skills.append(item.name)                       # Список всех навыков

            if key_skills:
                for item in key_skills:
                    if item['name'] in list_skills:
                        skill = Skill.objects.get(name=item['name'])
                        skill.count = skill.count + 1
                        skill.save()
                    else:
                        Skill.objects.create(name=item['name'], count=1)
                        post = Post.objects.get(name=text_vacancies)
                        # post.skill.set(Skill.objects.get(name=item['name']))

        print('End')
        # ***********************

        # post.area.set(Area.objects.all())
        # post.skill.set(Skill.objects.all())
