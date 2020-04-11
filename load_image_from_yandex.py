import requests
from bs4 import BeautifulSoup as bs

img_to_search = 'альпы'

r = requests.get(f"https://yandex.ru/images/search?from=tabbar&text={img_to_search}")

text = r.text

soup = bs(text, "html.parser")

for qwerty in soup.find_all('img'):
    if 'im0-tub-ru' in qwerty.get('src'):
        print(qwerty.get('src'))
        img = 'http:' + qwerty.get('src')
        break

p = requests.get(img)
out = open("img.jpg", "wb")
out.write(p.content)
out.close()
