from django.core.management.base import BaseCommand
from blogapp.models import Post, Skill, Area, Salary
import requests


class Command(BaseCommand):
    def handle(self, *args, **options):


        count = 0
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
        print('Отбор вакансий по запросу: ', text_vacancies)
        print('Всего найдено вакансий: ', found)
        print(f'Всего страниц: {pages}, Вакансий на странице: {per_page}')
        # pprint.pprint(result)
        p = 0
        # print('Вакансия ', p)
        item_one_vacancy = result['items'][p]
        one_vacancy_url = item_one_vacancy['url']
        result_one_vac = requests.get(one_vacancy_url).json()
        key_skills = result_one_vac['key_skills']                   # словарь ключевых навыков в вакансии
        salary = result_one_vac['salary']                         # словарь с данными по зарплате
        sity = result_one_vac['area']                               # словарь с названием города
        # print('город ', sity['name'])
        # print(key_skills)
        # print(Skill.objects.all())
        # ****************************************
        Post.objects.create(name=text_vacancies)                    # создаем query set объектов с вакансиями
        post = Post.objects.get(name=text_vacancies)                # получаем конкретную вакансии
        for item in key_skills:
            Skill.objects.create(name=item['name'], count=1)        # создаем query set объектов навыков
        skill = Skill.objects.all()  # получаем все навыки
        # post.skill.set(skill)                                     # определяем навыки конкретной вакансии
        Area.objects.create(name=sity['name'])                      # создаем query set объектов городов
        area = Area.objects.all()                                   # получаем все города
        # post.area.set(area)                                       # определяем города конкретной вакансии
        if salary and salary['currency'] == 'RUR' and salary['from']:
            if salary['to']:
                Salary.objects.create(salary_from=salary['from'], salary_to=salary['to'])
            else:
                Salary.objects.create(salary_from=salary['from'], salary_to=salary['from'])
        count += 1
        # ****************************************
        for p in range(1, 20):
            print('Вакансия: ', count)
            count += 1
            if count >= found:
                break
            # print('Вакансия ', p)
            item_one_vacancy = result['items'][p]
            one_vacancy_url = item_one_vacancy['url']
            result_one_vac = requests.get(one_vacancy_url).json()
            key_skills = result_one_vac['key_skills']               # словарь ключевых навыков в вакансии
            salary = result_one_vac['salary']                       # словарь с данными по зарплате
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
                        # post = Post.objects.get(name=text_vacancies)
                        # post.skill.set(Skill.objects.get(name=item['name']))
            if salary and salary['currency'] == 'RUR' and salary['from']:
                if salary['to']:
                    Salary.objects.create(salary_from=salary['from'], salary_to=salary['to'])
                else:
                    Salary.objects.create(salary_from=salary['from'], salary_to=salary['from'])

        # print('End')
        # ***********************
        # post.area.set(Area.objects.all())
        # post.skill.set(Skill.objects.all())
        for page in range(2, pages):

            params = {
                'text': text_vacancies,
                'page': page,
                'per_page': 20,
                'area': 113  # 113 - Россия
            }
            result = requests.get(url_vacancies, params=params).json()

            for p in range(20):
                count += 1
                if count >= found:
                    break
                print('Вакансия ', count)
                item_one_vacancy = result['items'][p]
                one_vacancy_url = item_one_vacancy['url']
                result_one_vac = requests.get(one_vacancy_url).json()
                key_skills = result_one_vac['key_skills']               # словарь ключевых навыков в вакансии
                salary = result_one_vac['salary']                       # словарь с данными по зарплате
                sity = result_one_vac['area']                           # словарь с названием города
                # ****************************************
                list_sities = []
                sities = Area.objects.all()
                for item in sities:
                    list_sities.append(item.name)
                if sity['name'] not in list_sities:
                    Area.objects.create(name=sity['name'])

                list_skills = []
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
                            # post = Post.objects.get(name=text_vacancies)
                            # post.skill.set(Skill.objects.get(name=item['name']))
                if salary and salary['currency'] == 'RUR' and salary['from']:
                    if salary['to']:
                        Salary.objects.create(salary_from=salary['from'], salary_to=salary['to'])
                    else:
                        Salary.objects.create(salary_from=salary['from'], salary_to=salary['from'])


        post.area.set(Area.objects.all())                         # определяем все города конкретной вакансии
        post.skill.set(Skill.objects.all())                       # определяем все навыки конкретной вакансии