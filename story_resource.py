from data import db_session
from flask import jsonify, abort
from flask_login import UserMixin
from flask_restful import Resource
import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from story_parser import parser


class Story(db_session.SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'stories'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)  # название истории
    text = sqlalchemy.Column(sqlalchemy.String)  # текст истории
    answer = sqlalchemy.Column(sqlalchemy.String)  # ответ на задачу
    spectator = sqlalchemy.Column(sqlalchemy.String)  # опрос очевидцев
    opinion = sqlalchemy.Column(sqlalchemy.String)  # мнение коллег
    api = sqlalchemy.Column(sqlalchemy.String)  # вид API
    proof = sqlalchemy.Column(sqlalchemy.String)  # объект поиска API
    answer_choice = sqlalchemy.Column(sqlalchemy.String)  # строка, разделенная _


def abort_if_story_not_found(story_id):
    session = db_session.create_session()
    story = session.query(Story).get(story_id)
    if not story:
        abort(404, message=f"Story {story_id} not found")


class StoryResource(Resource):
    def get(self, story_id):
        abort_if_story_not_found(story_id)
        session = db_session.create_session()
        story = session.query(Story).get(story_id)
        return jsonify({'stories': story.to_dict()})

    def delete(self, story_id):
        abort_if_story_not_found(story_id)
        session = db_session.create_session()
        story = session.query(Story).get(story_id)
        session.delete(story)
        session.commit()
        return jsonify({'success': 'OK'})


class StoryListResource(Resource):
    def get(self):
        session = db_session.create_session()
        story = session.query(Story).all()
        return jsonify({'stories': [item.to_dict() for item in story]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        story = Story(
            id=args['id'],
            title=args['title'],
            text=args['text'],
            answer=args['answer'],
            spectator=args['spectator'],
            opinion=args['opinion'],
            api=args['api'],
            proof=args['proof'],
            answer_choice=args['answer_choice']
        )
        session.add(story)
        session.commit()
        return jsonify({'success': 'OK'})
