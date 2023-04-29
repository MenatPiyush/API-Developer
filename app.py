from flask import Flask
from flask_cors import CORS
import resolver 
from flask_graphql import GraphQLView

app = Flask(__name__)
CORS(app)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=resolver.schema,
        graphiql=True
    ),
)
