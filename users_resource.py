from data import db_session
from flask import jsonify, abort
from flask_login import UserMixin
from flask_restful import Resource
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from user_parser import parser


class User(db_session.SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    nickname = sqlalchemy.Column(sqlalchemy.String)
    password = sqlalchemy.Column(sqlalchemy.String)
    submit = sqlalchemy.Column(sqlalchemy.Boolean)
    watched = sqlalchemy.Column(sqlalchemy.String)

    def check_password(self, password):
        if password == self.password:
            return True
        return False


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
            id=args['id'],
            nickname=args['nickname'],
            password=args['password'],
            submit=args['submit'],
            watched=args['watched']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
