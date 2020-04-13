from requests import get, post, delete

print(get('http://localhost:5000/api/stories').json())  # все истории

print(get('http://localhost:5000/api/stories/1').json())  # одна история

print(delete('http://localhost:5000/api/stories/2').json())  # удалить историю

text = ' '.join(['Охотник прицелился и выстрелил.',
                 'Через несколько секунд он понял, что совершил ужасную ошибку.',
                 'Через пару минут он был мертв.'])

print(post('http://localhost:5000/api/stories',  # добавить историю
           json={'id': 1,
                 'title': 'Осознание ошибки',
                 'text': text,
                 'answer': 'лавина в горах',
                 'spectator': '',
                 'opinion': '',
                 'api': 'image',
                 'proof': 'альпы',
                 'answer_choice': 'лавина в горах_медведь_война_неисправное ружье'}).json())

print(get('http://localhost:5000/api/stories/5').json())  # несуществующая история

print(get('http://localhost:5000/api/stories/q'))  # неверный запрос (ошибка 404)

print(post('http://localhost:5000/api/stories',  # не все параметры
           json={'id': 1,
                 'text': '''Охотник прицелился и выстрелил.
                 Через несколько секунд он понял, что совершил ужасную ошибку.
                 Через пару минут он был мертв.''',
                 'api': 'image',
                 'proof': 'альпы'}).json())
