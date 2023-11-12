import requests
import pprint

def parse(text_vacancies):
    # text_vacancies = 'junior AND (js) AND (Москва)'
    # text_vacancies = 'js developer'
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
    # print('Всего найдено вакансий: ', found)
    # print(f'Всего страниц: {pages}, Вакансий на странице: {per_page}')
    #pprint.pprint(result)
    p = 1
    # pprint.pprint(result)[p]
    item_one_vacancy = result['items'][p]
    one_vacancy_url = item_one_vacancy['url']
    result_one_vac = requests.get(one_vacancy_url).json()
    key_skills = result_one_vac['key_skills']
    salary = result_one_vac['salary']
    area = result_one_vac['area']
    vac_name = result_one_vac['name']
    print(vac_name)
    # pprint.pprint(item_one_vacancy)
    pprint.pprint(result_one_vac)
    print(f'вакансия {p}')
    pprint.pprint(key_skills)
    #pprint.pprint(result_one_vac)
    pprint.pprint(salary)
    pprint.pprint(area)
    return key_skills, area, salary

if __name__ == '__main__':
    parse('python developer')
