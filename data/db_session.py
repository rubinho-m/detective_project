import os
import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as dec

from sqlalchemy.orm import Session

SqlAlchemyBase = dec.declarative_base()

__factory = None

address = 'sqlite:///db/detective.db?check_same_thread=False'

k = 0


def global_init():
    global __factory
    global address

    if __factory:
        return

    if 'DATABASE_URL' in os.environ:
        conn_str = os.environ['DATABASE_URL']  # сработает на Heroku
    else:
        conn_str = address  # 'sqlite:///db/detective.db?check_same_thread=False'

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    global k
    # k += 1
    # if k != 1:
    #     bd = 'postgres://hltznebfnqgzrn:5789bca7a95dc1df252d4bb9fbc643230e5d37d6fd202a972a93f812bb4240e3@ec2-52-44-55-63.compute-1.amazonaws.com:5432/d1qfd3iejflmpl'
    #     engine = sa.create_engine(bd, echo=False)
    #     __factory = orm.sessionmaker(bind=engine)
    return __factory()
