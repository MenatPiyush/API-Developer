import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from models import Post as PostModel

class Post(SQLAlchemyObjectType):
    class Meta:
        model = PostModel
        interfaces = (graphene.relay.Node,)
        
class PostAttributes:
    id = graphene.Int()
    
class CreatePostInput(graphene.InputObjectType, PostAttributes):
    pass
