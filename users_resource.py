import sqlalchemy

from flask import jsonify, abort
from flask_login import UserMixin
from flask_restful import Resource
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from user_parser import parser
from data import db_session


class User(db_session.SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    nickname = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)
    submit = sqlalchemy.Column(sqlalchemy.Boolean)
    watched = sqlalchemy.Column(sqlalchemy.String)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def add_story(self, story):
        if self.watched is not None:
            if story not in str(self.watched):
                self.watched = str(self.watched) + ' ' + story
        else:
            self.watched = ' '.join([story])


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({'users': user.to_dict()})

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'users': [item.to_dict() for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            nickname=args['nickname'],
            password=args['password'],
            submit=args['submit'],
            watched=args['watched']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
