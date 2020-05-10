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
    # global k
    # k += 1
    # if k != 1:
    #     bd = 'postgres://kcxclqidxjcndn:b58edf0876605b6ed9b14d32e01bea475fb7c26c769ecd6c5312aeae3367fec0@ec2-35-171-31-33.compute-1.amazonaws.com:5432/deardkh58mhgrk'
    #     engine = sa.create_engine(bd, echo=False)
    #     __factory = orm.sessionmaker(bind=engine)
    return __factory()
