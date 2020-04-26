import requests
from bs4 import BeautifulSoup as bs


def load_image(img_to_search, user):
    r = requests.get(f"https://yandex.ru/images/search?from=tabbar&text={img_to_search}")

    text = r.text

    soup = bs(text, "html.parser")

    for qwerty in soup.find_all('img'):
        if 'im0-tub-ru' in qwerty.get('src'):
            print(qwerty.get('src'))
            img = 'http:' + qwerty.get('src')
            break

    p = requests.get(img)
    map_file = f'static/loaded/{user}.jpg'
    out = open(map_file, "wb")
    out.write(p.content)
    out.close()
    return map_file
