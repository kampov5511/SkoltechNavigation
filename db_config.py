from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

Base = declarative_base()

engine = create_engine('sqlite:///nazi.db?check_same_thread=False', poolclass=NullPool)


class User(Base):
    __tablename__ = 'user'

    id = Column(String, primary_key=True)
    chat_id = Column(String)
    state = Column(Integer, nullable=True)
    destination = Column(Integer, nullable=True)


class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey(User.id))
    text = Column(String)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

