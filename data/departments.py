from .db_session import SqlAlchemyBase
import sqlalchemy


class Departments(SqlAlchemyBase):
    __tablename__ = 'departments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("jobs.team_leader"))
    members = sqlalchemy.Column(sqlalchemy.String,
                                sqlalchemy.ForeignKey("users.id"))
    email = sqlalchemy.Column(sqlalchemy.String, unique=True)
