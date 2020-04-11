from requests import get, post, delete

print(get('http://localhost:5000/api/users').json())  # все пользователи

print(get('http://localhost:5000/api/users/1').json())  # один пользователь

print(delete('http://localhost:5000/api/users/2').json())  # удалить пользователя

print(post('http://localhost:5000/api/users',  # добавить пользователя
           json={'id': 4,
                 'nickname': 'new_user',
                 'password': 'qwerty',
                 'submit': None,
                 'watched': None}).json())

print(get('http://localhost:5000/api/users/5').json())  # несуществующий пользователь

print(get('http://localhost:5000/api/users/q'))  # неверный запрос (ошибка 404)

print(post('http://localhost:5000/api/users',  # не все параметры
           json={
               'email': 'simple_email@mail.ru',
               'password': 'qwerty',
               'remember_me': None,
               'submit': None,
               'city': 'London'}).json())
