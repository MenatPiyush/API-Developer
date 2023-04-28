from graphql import GraphQLError
from graphene import ObjectType, Schema, Field, List, ID, String, DateTime, Boolean, Mutation
from resolver import get_current_user
from models import User,Post,PostComment
class CreatePost(Mutation):
    class Arguments:
        title = String(required=True)
        content = String(required=True)

    post = Field(Post)

    @jwt_required
    def mutate(self, info, title, content):
        current_user = get_current_user()
        user = User.get_query(info).filter_by(id=current_user['user_id']).first()

        if not user:
            raise GraphQLError('Invalid user')

        post = Post(title=title, content=content, author=user)
        session.add(post)
        session.commit()

        return CreatePost(post=post)