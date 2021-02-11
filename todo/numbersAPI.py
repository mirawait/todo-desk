import requests

def get_fact(month,day):
    response = requests.get(f'http://numbersapi.com/{month}/{day}/date')
    return response.text
