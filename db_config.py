from sqlalchemy import create_engine
from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import NullPool

Base = declarative_base()

engine = create_engine('sqlite:///nazi.db', poolclass=NullPool)


class User(Base):
    __tablename__ = 'user'

    id = Column(String, primary_key=True)
    chat_id = Column(String)
    state = Column(Integer, nullable=True)
    destination = Column(Integer, nullable=True)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

