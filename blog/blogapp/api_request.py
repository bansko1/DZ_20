import requests
import pprint

# response = requests.get('http://127.0.0.1:8000/api/v0/vacancy/', auth=('max', 'maxmaxmax')) # Аутентификация в запросе по логину и паролю
# pprint.pprint(response.json())

token = '1166b95af2fc31a7439df9cdd7a4b55ec19f8e5e'
headers = {'Authorization': f'Token {token}'}
response = requests.get('http://127.0.0.1:8000/api/v0/area/', headers=headers) # Аутентификация в запросе по токену
# response = requests.get('http://127.0.0.1:8000/api/v0/vacancy/') # Аутентификация в запросе по токену
pprint.pprint(response.json())