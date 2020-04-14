from data import db_session
from flask import Flask, render_template, url_for
from flask_restful import abort, Api
from users_resource import User, UserResource, UserListResource
from story_resource import Story, StoryResource, StoryListResource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_detective_key'
api = Api(app)

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
   return render_template('base.html', current_user=current_user, css_style=url_for('static', filename='css/style.css'))


if __name__ == '__main__':
    main()
