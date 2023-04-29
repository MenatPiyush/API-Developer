from datetime import datetime, timedelta
from graphene import ObjectType,Field, List,String,Mutation, Int, Schema
from models import User,Post
from user_auth import Session, validate_user,SECRET_KEY
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
import jwt

class PostSchema(SQLAlchemyObjectType):
    class Meta:
        model = Post
        interfaces = (relay.Node,)
    
class UserSchema(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node,)
        

class Query(ObjectType):
    posts = List(lambda: PostSchema)
    post = Field(lambda: PostSchema, id=String(required=True))
    
    
    def resolve_posts(self,info):
        session = Session()
        posts = session.query(Post).all()
        return posts
    
    def resolve_post(self,info,id):
        session = Session()
        post = session.query(Post).filter_by(id=id).first()
        return post

class Signup(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        
    user = String()
    
    def mutate(self,info,username, email, password):
        created_at = datetime.now()
        new_user = username
        user = User(username=username, email=email, password=password, created_at = created_at)
        session = Session()
        session.add(user)
        session.commit()
        return Signup(user = new_user)
        
class CreatePost(Mutation):
    class Arguments:
        title = String(required = True)
        content = String(required = True)
        
    post = Field(PostSchema)
        
    def mutate(self,info,title,content):
        auth_header = info.context.headers.get('Authorization')
        token = auth_header.split(' ')[1] if auth_header else None
        user_id = validate_user(token=token)
        if user_id!= None:
            post = Post(title=title, content=content, author_id=user_id)
            session = Session()
            session.add(post)
            session.commit()
            return CreatePost(post)
        else:
            return("User not allowed")       
    
    

class UpdatePost(Mutation):
    class Arguments:
        id = Int(required = True)
        title = String(required=True)
        content = String(required=True)
    
    msg = String()

    def mutate(self,info, id,title, content):
        auth_header = info.context.headers.get('Authorization')
        token = auth_header.split(' ')[1] if auth_header else None
        user_id = validate_user(token = token)
        session = Session()
        post = session.query(Post).filter_by(author_id = user_id, id = id).first()
        if post:
            post.title = title
            post.content = content
            session.add(post)
            session.commit()
            msg = "Post updated successfully"
            return UpdatePost(msg = msg)
        else:
            msg = "User not allowed"
            return UpdatePost(msg = msg)
  
class DeletePost(Mutation):
    class Arguments:
        id = Int(required = True)
    
    msg = String()
    def mutate(self, info,id):
        auth_header = info.context.headers.get('Authorization')
        token = auth_header.split(' ')[1] if auth_header else None
        user_id = validate_user(token = token)
        session = Session()
        post = session.query(Post).filter_by(author_id = user_id, id = id).first()
        if post:
            print(post)
            session.delete(post)
            session.commit()
            msg="Post deleted"
            return DeletePost(msg=msg)
        else:
            msg="Post does not exist or user is not authorized"
            return DeletePost(msg=msg)

class Login(Mutation):
    class Arguments:
        username = String(required=True)
        password = String(required=True)
    
    token = String()
    msg = String()

    def mutate(self,info,username, password):
        session = Session()
        user = session.query(User).filter_by(username=username).first()
        if password == user.password:
            payload = {
                'username': str(user.username),
                'exp': datetime.utcnow() + timedelta(days=1)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return Login(token = token)
        else:
            msg = "User not allowed"
            return Login(msg = msg)

 
class Mutation(ObjectType):
    signup = Signup.Field() 
    login = Login.Field()   
    createpost = CreatePost.Field()
    deletePost = DeletePost.Field()
    updatepost = UpdatePost.Field()
    
schema = Schema(query=Query,mutation=Mutation)