from data import db_session
from flask import Flask
from flask_restful import abort, Api
from users_resource import User, UserResource, UserListResource
from story_resource import Story, StoryResource, StoryListResource

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandex_detective_key'
api = Api(app)


def main():
    db_session.global_init("db/detective.db")
    api.add_resource(UserListResource, '/api/users')
    api.add_resource(UserResource, '/api/users/<int:user_id>')
    api.add_resource(StoryListResource, '/api/stories')
    api.add_resource(StoryResource, '/api/stories/<int:story_id>')
    app.run()


if __name__ == '__main__':
    main()
