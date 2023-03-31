import requests as r
import geopy
import os
from datetime import datetime


def git_search(query, language):
    url = 'https://api.github.com/search/repositories'
    params = {'q': query,
              'l': language}
    res = r.get(url, params=params).json()
    message = ''
    for repo in res['items']:
        message += f'<a href="{repo["svn_url"]}">{repo["name"]}</a>\n'
    return message


def get_image():
    content = r.get('https://random.dog/woof.json').json()
    url = content['url']
    return url


def get_city(lat, lon):
    locator = geopy.geocoders.Nominatim(user_agent='geoapiExercises')
    location = locator.reverse(str(lat) + "," + str(lon))
    address = location.raw['address']
    return address


def save_user_info(text):
    with open('users.txt', 'a') as file:
        file.write(text)

def read_text(filename):
    with open(filename, 'r') as file:
        res = file.read()
    return res


def get_forecast(lat, long):
    url = 'https://api.openweathermap.org/data/2.5/forecast'
    params = {
        'lat': lat,
        'lon': long,
        'appid': os.environ.get('WEATHER_KEY'),
        'units': 'metric',
        'lang': 'ru',
    }
    resp = r.get(url, params=params).json()
    text = '<strong>{}</strong> <i>{}</i>: \n{}C, {}\n\n'
    res = ''

    for data in resp['list']:
        date = datetime.fromtimestamp(data['dt'])  # конвертируем timestamp в дату
        date_res = date.strftime('%d.%m.%y')  # 31.03.2023
        temp = data['main']['temp']
        weather = data['weather'][0]['description']
        if date.hour == 15:
            daytime = 'днём'
            res += text.format(date_res, daytime, temp, weather)
        elif date.hour == 21:
            daytime = 'вечером'
            res += text.format(date_res, daytime, temp, weather)
    return res
