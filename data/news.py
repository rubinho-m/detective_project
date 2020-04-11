from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField, BooleanField, StringField, TextAreaField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    teamlead_id = StringField('ID тимлида')
    work_size = StringField("Размер работы")
    collaborators = StringField("Помощники")
    submit = SubmitField('Применить')


