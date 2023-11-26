from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from blogapp.models import Skill, Area, Word, Vacancy, Word_skill
import requests


class Command(BaseCommand):
    def __init__(self, vacancy, pages, user):
        super().__init__()
        self.vac = vacancy
        self.pages = pages
        self.user = user

    def handle(self, *args, **options):

        count = 0
        count_perc = 0
        list_sities = []
        list_skills = []
        list_words = []
        list_vacancy = []
        # text_vacancies = 'python developer'    # Название вакансии
        # text_vacancies = 'python developer'          # Название вакансии
        text_vacancies = self.vac  # Название вакансии
        user_name = self.user  # Название юзера
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
        print('Отбор вакансий по запросу: ', text_vacancies)
        print('Всего найдено вакансий: ', found)
        print(f'Всего страниц: {pages}, Вакансий на странице: {per_page}')

        # ****************************************
        try:
            word = Word.objects.get(name=text_vacancies)
        except ObjectDoesNotExist:
            word = Word.objects.create(name=text_vacancies, count=found,
                                       user=user_name)  # создаем query set объектов с вакансиями
            print('Запрос:', word)

        for page in range(self.pages):  # Просмотр первых 10 страниц (по 20 вакансий)
            params = {
                'text': text_vacancies,
                'page': page,
                'per_page': 20,
                'area': 113  # 113 - Россия
            }
            result = requests.get(url_vacancies, params=params).json()

            for p in range(20):  # обработка 20 вакансий на странице
                count += 1
                if count >= found:
                    break

                print('Вакансия ', count)
                item_one_vacancy = result['items'][p]
                one_vacancy_url = item_one_vacancy['url']
                result_one_vac = requests.get(one_vacancy_url).json()
                # name_vacancy = result_one_vac['name']                 # название вакансии
                key_skills = result_one_vac['key_skills']  # список словарей ключевых навыков в одной вакансии
                salary = result_one_vac['salary']  # словарь с данными по зарплате
                sity = result_one_vac['area']  # словарь с названием города
                vac_name = result_one_vac['name']
                # url = item_one_vacancy
                print(vac_name)
                # ****************************************
                # word = Word.objects.get(name=text_vacancies)

                try:
                    area = Area.objects.get(name=sity['name'], id_word=word)
                except ObjectDoesNotExist:
                    area = Area.objects.create(name=sity['name'], id_word=word)  # Создание объекта "город"
                print(area)

                skills = Skill.objects.all()
                if key_skills:
                    for item in key_skills:
                        try:
                            skill = Skill.objects.get(name=item['name'])
                        except ObjectDoesNotExist:
                            skill = Skill.objects.create(name=item['name'])  # Создание объекта "навык"
                        print(skill)

                # if key_skills:
                #     for item in key_skills:
                #         if item['name'] not in list_skills:
                #             skill = Skill.objects.create(name=item['name'])  # Создание объектов "навыки"
                #             print(skill)

                if vac_name not in list_vacancy:
                    list_vacancy.append(vac_name)
                    # print(list_vacancy)

                    if salary and salary['currency'] == 'RUR' and salary['from']:
                        salary_from = salary['from']
                        if salary['to']:
                            salary_to = salary['to']
                        # Salary.objects.create(salary_from=salary['from'], salary_to=salary['to'])
                        else:
                            salary_to = salary['from']
                    else:
                        salary_from = 0
                        salary_to = 0
                    vacancy = Vacancy.objects.create(name=vac_name, salary_from=salary_from, salary_to=salary_to,
                                                     word=word, area=area, url=item_one_vacancy[
                            'alternate_url'])  # Создание объекта "вакансия"

                    print(vacancy)

                # word = Word.objects.get(name=text_vacancies)
                for item in key_skills:
                    count_perc += 1
                    skill = Skill.objects.get(name=item['name'])
                    print(word, skill)
                    r = Word_skill.objects.filter(id_word=word, id_skill=skill).first()
                    if not r:
                        new = Word_skill.objects.create(id_word=word, id_skill=skill,
                                                        count=1.0, percent=0.0)  # Создание объекта "навыки по запросам"

                        print('w_s done', new.count)
                    else:
                        r.count += 1
                        r.save()
                        print('w_s not edit', r.count)
                    print(count_perc)


