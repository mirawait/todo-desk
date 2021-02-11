import requests


def get_weather(city):
    response = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=d79db2831d17bf14e56373c865e16bc7").json()
    weather = {'curr_temp': response['main']['temp'], 'feels_like': response['main']['feels_like'],
               'cloudiness': response['weather'][0]['main']}
    return weather
