import os

from flask import Flask, render_template, url_for, redirect
from flask_restful import abort, Api
from flask import session as user_ses
from flask_login import LoginManager, login_required, logout_user, login_user
from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField, BooleanField, SubmitField
from wtforms.fields.core import StringField
from wtforms.validators import DataRequired

from requests import get, post, delete

from get_img import get_img

from data import db_session
from users_resource import User, UserResource, UserListResource
from story_resource import Story, StoryResource, StoryListResource
from load_image_from_yandex import load_image
from delete_loaded_img import delete_in_directory as del_imgs


class RegisterForm(FlaskForm):
    nickname = StringField("Никнейм", validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторный пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    nickname = StringField('Никнейм', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_detective_key'
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)


def download_all():  # download all images from yandex for heroku. do it just once
    session = db_session.create_session()
    stories = session.query(Story).all()
    for story in stories:
        story = story.to_dict()
        if story['api'] == 'image':
            load_image(story['proof'], story['id'])


def capitalize_first(string):
    if string:
        return string[0].upper() + string[1:]
    return string[:]


def main():
    db_session.global_init()
    api.add_resource(UserListResource, '/api/users')
    api.add_resource(UserResource, '/api/users/<int:user_id>')
    api.add_resource(StoryListResource, '/api/stories')
    api.add_resource(StoryResource, '/api/stories/<int:story_id>')
    if "PORT" in os.environ:
        app.run(host='0.0.0.0', port=os.environ["PORT"])
    else:
        # download_all()
        # session = db_session.create_session()
        # stories = session.query(Story).all()
        # session.close()
        # for i in range(len(stories)):
        #     print(i)
        #     story = stories[i].to_dict()
        #     session = db_session.create_session()
        #     new = Story(
        #         id=None,
        #         title=story['title'],
        #         text=story['text'],
        #         answer=story['answer'],
        #         spectator=story['spectator'],
        #         opinion=story['opinion'],
        #         api=story['api'],
        #         proof=story['proof'],
        #         api_message=story['api_message'],
        #         answer_choice=story['answer_choice']
        #     )
        #     session.add(new)
        #     session.commit()
        app.run(host='127.0.0.1', port=5000)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()

    return session.query(User).get(user_id)


@app.route("/")
@app.route('/index')
def start():
    session = db_session.create_session()
    user = session.query(User).get(user_ses.get('current_user'))
    if user and user.watched is not None:
        stories = [int(x) for x in str(user.watched).split()]
    else:
        stories = None

    all_stories = session.query(Story).all()

    all_stories = list(map(lambda x: x.to_dict(), all_stories))

    all_stories = sorted(all_stories, key=lambda x: x['id'])

    # all_stories = sorted(all_stories, all_stories)
    return render_template('index.html',
                           background=url_for('static', filename='img/bg.jpg'),
                           stories=all_stories,
                           user_stories=stories)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.nickname == form.nickname.data).first()
        if 'current_user' in user_ses:
            user_ses['current_user'] = user_ses.get('current_user')
        else:
            user_ses['current_user'] = user.id
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form,
                           background=url_for('static', filename='img/mbg.jpg'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data == form.password_again.data:
            session = db_session.create_session()
            user = User()

            user.nickname = form.nickname.data
            user.set_password(form.password.data)

            session.merge(user)
            session.commit()
            return redirect('/')
        return render_template('register.html',
                               message="Пароли не совпадают",
                               form=form)
    return render_template('register.html', title='Регистрация', form=form,
                           background=url_for('static', filename='img/mbg.jpg'))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@app.route('/story_telling/<int:id>')
@login_required
def tell(id):
    path = 'static/loaded'
    del_imgs(path)

    session = db_session.create_session()
    story = session.query(Story).get(id)
    # story = get(f'http://localhost:5000/api/stories/{id}').json()['stories']

    picture_list = []

    pictures = story.proof.split('_')
    if story.api == 'image':
        for pict in pictures:
            picture_list.append(f'/static/loaded/{id}.jpg')
    elif story.api == 'map':
        for map in pictures:
            picture_list.append(f'/{get_img(map)}')
    temp = []
    for answ in story.answer_choice.split('_'):
        new = capitalize_first(answ)
        temp.append(new)
    story.answer_choice = '_'.join(temp)
    story.answer = capitalize_first(story.answer)
    return render_template('story.html',
                           background=url_for('static', filename='img/mbg.jpg'),
                           story=story,
                           picture_list=picture_list)


@app.route('/right_ans/<int:id>')
@login_required
def right_answer(id):
    session = db_session.create_session()
    story = session.query(Story).get(id)

    user = session.query(User).get(user_ses.get('current_user'))
    user.add_story(str(story.id))

    session.commit()
    return render_template('win.html', background=url_for('static', filename='img/mbg.jpg'))


@app.route('/wrong_ans')
@login_required
def wrong_answer():
    return render_template('false.html', background=url_for('static', filename='img/mbg.jpg'))


@app.route('/logout')
@login_required
def logout():
    user_ses.pop('current_user', None)

    logout_user()
    return redirect("/")


if __name__ == '__main__':
    main()
