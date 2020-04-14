from data import db_session
from flask import Flask, render_template, url_for, redirect
from flask_restful import abort, Api
from users_resource import User, UserResource, UserListResource
from story_resource import Story, StoryResource, StoryListResource
from flask_login import LoginManager, login_required, logout_user, login_user


from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField, BooleanField, SubmitField
from wtforms.fields.core import StringField
from wtforms.validators import DataRequired


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

current_user = None


def main():
    db_session.global_init("db/detective.db")
    api.add_resource(UserListResource, '/api/users')
    api.add_resource(UserResource, '/api/users/<int:user_id>')
    api.add_resource(StoryListResource, '/api/stories')
    api.add_resource(StoryResource, '/api/stories/<int:story_id>')
    app.run()


@app.route("/")
@app.route('/index')
def start():
   return render_template('base.html', current_user=current_user,
                          css_style=url_for('static', filename='css/style.css'),
                          background=url_for('static', filename='img/img_start.jpg'))


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()

    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    global current_user

    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.nickname == form.nickname.data).first()
        if user and user.check_password(form.password.data):
            current_user = user
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


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
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    global current_user

    logout_user()
    current_user = None
    return redirect("/")


if __name__ == '__main__':
    main()
