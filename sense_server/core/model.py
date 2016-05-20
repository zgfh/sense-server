import sqlalchemy as sa
import datetime
from sqlalchemy import Column

from sense_server.db import Base, session_scope

ZERO_TIMESTAMP = datetime.datetime(1970, 1, 2)


class Post(Base):
    __tablename__ = "post"
    id = Column(sa.String(255), primary_key=True)
    read_ts = Column(sa.TIMESTAMP)
    is_favorite = Column(sa.BOOLEAN)

    def __init__(self, id, read_ts=None, is_favorite=False):
        self.id = id
        if read_ts is None:
            self.read_ts = ZERO_TIMESTAMP

        self.is_favorite = is_favorite

    def to_dict(self):
        return {
            "id": self.id,
            "read_ts": self.read_ts,
            "is_favorite": self.is_favorite
        }


def list_favorite_post():
    with session_scope() as session:
        return session.query(Post).filter_by(is_favorite=True).all()


def list_read_post():
    with session_scope() as session:
        return session.query(Post).filter(Post.read_ts > ZERO_TIMESTAMP).all()


def remove_favorites(ids):
    with session_scope(force_close=True) as session:
        for id in ids:
            p = get_post(id)
            if p:
                p.is_favorite = False


def get_post(id):
    with session_scope() as session:
        return session.query(Post).filter_by(id=id).first()


def read_post(id):
    with session_scope(force_close=True) as session:
        post = get_post(id)
        if not post:
            p = Post(id, read_ts=datetime.datetime.now())
            session.add(p)
            return p

        post.read_ts = datetime.datetime.now()
        return post


def unread_post(id):
    with session_scope(force_close=True) as session:
        post = get_post(id)
        if not post:
            return
        post.read_ts = ZERO_TIMESTAMP
        return post


def add_favorites(ids):
    with session_scope(force_close=True) as session:
        for id in ids:
            p = get_post(id)
            if p:
                p.is_favorite = True
            else:
                p = Post(id=id, is_favorite=True)
                session.add(p)

        return None
