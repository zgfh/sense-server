import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from sqlalchemy.orm import scoped_session
from .settings import DATABASE
from flask import g

ENGINE = sqlalchemy.create_engine(DATABASE, echo=False, pool_size=5, pool_recycle=3600, encoding='utf8',
                                  convert_unicode=True,
                                  connect_args={'charset': 'utf8'})

Session = scoped_session(sqlalchemy.orm.session.sessionmaker(bind=ENGINE, expire_on_commit=False))
METADATA = MetaData()
Base = declarative_base(metadata=METADATA)


@contextmanager
def session_scope(force_close=False):
    session = __get_db_session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        close_session()
        raise
    finally:
        if not getattr(session, "session_nested", False) or force_close:
            session.expunge_all()
            close_session()


def __get_db_session():
    if hasattr(g, 'db_session') and g.db_session is not None:
        setattr(g.db_session, "session_nested", True)
        return g.db_session
    else:
        g.db_session = Session()
        return g.db_session


def close_session():
    if hasattr(g, 'db_session'):
        g.db_session.close()
        delattr(g, 'db_session')
