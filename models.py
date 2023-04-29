from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True)
    username = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    #posts = relationship('Post',back_populates='author_id')
    #comments = relationship('PostComment', back_populates='author_id')
    
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
    #author = relationship('User', back_populates='posts')
    #comments = relationship('PostComment',back_populates='posts')
    
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
    #author = relationship('User',back_populates='comments')
    #post = relationship('Post',back_populates='comments')
  

#User.posts = relationship("Post", order_by=Post.id, back_populates="author")
#User.comments = relationship("PostComment", order_by=PostComment.id, back_populates="author")
#Post.comments = relationship("PostComment", order_by=PostComment.id, back_populates="post")    