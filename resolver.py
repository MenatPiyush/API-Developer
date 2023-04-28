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

class UpdatePost(Mutation):
    class Arguments:
        id = Int(required = True)
        title = String(required=True)
        content = String(required=True)

    post = Field(Post)

    def mutate(id,title, content,token):
        user_id = validate_user(token = token)
        if user_id!= None:
            session = Session()
            session.query(Post).filter(id = id).update(title =title,content =content)
            return ("Post updated")
        else:
            return("User not allowed")
  
   