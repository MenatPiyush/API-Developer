from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine(os.environ['DATABASE_URL'])
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    def __repr__(self):
        return f"<User {self.username}>"

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer,primary_key=True)
    title = Column(String)
    content = Column(String)
    author_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    def __repr__(self):
        return f"<User {self.title}>"
    
class PostComment(Base):
    __tablename__ = 'postcomment'
    id = Column(Integer, primary_key= True)
    content = Column(String)
    author_id = Column(Integer)
    post_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)