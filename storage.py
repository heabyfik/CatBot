from random import randint

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///sqlite3.db")

Base = declarative_base()
Session = sessionmaker(bind=engine)


class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True)

    path = Column(String)
    chat_id = Column(Integer)
    description = Column(String)

    def __init__(self, path, chat_id, description):
        self.path = path
        self.chat_id = chat_id
        self.description = description


def get_random_photo():
    session = Session()

    c = session.query(Photo.id).count()
    i = randint(1, c)
    p = session.query(Photo).filter(Photo.id == i).first()

    return p


def add_photo(p: Photo):
    session = Session()

    session.add(p)
    session.commit()


def _create_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    _create_db()
