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
    #     bd = 'postgres://eitmbruyscybfa:c93a936bdd50955a4a3d8a2b8d51a388d7922233a319a6fe23b001222afbe3d6@ec2-54-88-130-244.compute-1.amazonaws.com:5432/d1770t6u5ngl83'
    #     engine = sa.create_engine(bd, echo=False)
    #     __factory = orm.sessionmaker(bind=engine)
    return __factory()
