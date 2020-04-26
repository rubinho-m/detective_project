import requests
import random
from spn_selection import get_spn


def get_img(name):
    s = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={name}&format=json"
    response = requests.get(s)
    if not response:
        return 'ERROR: Некорректное имя объекта'
    json_response = response.json()
    if \
            json_response["response"]["GeoObjectCollection"]["metaDataProperty"][
                "GeocoderResponseMetaData"][
                "found"] == '0':
        return 'ERROR: Некорректное имя объекта\nБот ничего не нашел'
    toponym_coodrinates = \
        json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"][
            "pos"]
    toponym_coodrinates = toponym_coodrinates.split()
    x, y = toponym_coodrinates[0], toponym_coodrinates[1]
    first, second = get_spn(name)

    map_request = f"https://static-maps.yandex.ru/1.x/?l=map&pt={x},{y},pm2dol&spn={first},{second}"

    response = requests.get(map_request)

    map_file = f"static/loaded/map{random.randint(0, 2 ** 64)}.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file
