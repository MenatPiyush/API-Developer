from datetime import datetime
from graphene import ObjectType,Field, List, ID, String,Mutation, Int
from models import User,Post
from user_auth import Session, validate_user

class Query(ObjectType):
    posts = List(lambda: Post)
    post = Field(lambda: Post, id=ID(required=True))
    
    def resolve_posts():
        session = Session()
        posts = session.query(Post).all()
        result = [post for post in posts]
        return (result)
    
    def resolve_post(id):
        session = Session()
        post = session.query(Post).filter_by(id=id).first()
        return post

class Signup(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        
    def mutate(username, email, password, id):
        session = Session()
        created_at = datetime.now()
        user = User(id = id,username=username, email=email, password=password, created_at = created_at)
        session.add(user)
        session.commit()
        print("User Created")
        
class CreatePost(Mutation):
    class Arguments:
        title = String(required = True)
        content = String(requred = True)
        
    post = Field(Post)
        
    def mutate(title,content,token):
        user_id = validate_user(token=token)
        if user_id!= None:
            post = Post(title=title, content=content, author_id=user_id)
            session = Session()
            session.add(post)
            session.commit()
            return("Post Created")
        else:
            return("User not allowed")       
    
    

class UpdatePost(Mutation):
     class Arguments:
         id = Int(required = True)
         title = String(required=True)
         content = String(required=True)

     def mutate(id,title, content,token):
        user_id = validate_user(token = token)
        session = Session()
        post = session.query(Post).filter_by(author_id = user_id, id = id).first()
        if post:
            print(post)
            post.title = title
            post.content = content
            session.add(post)
            session.commit()
            return ("Post updated")
        else:
            return("User not allowed")
  
class DeletePost(Mutation):
    class Arguments:
        id = Int(required = True)
    
    def mutate(id,token):
        user_id = validate_user(token = token)
        session = Session()
        post = session.query(Post).filter_by(author_id = user_id, id = id).first()
        if post:
            print(post)
            session.delete(post)
            session.commit()
            return ("Post deleted")
        else:
            return("Post does not exist or user is not authorized")