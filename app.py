from flask import Flask,request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import resolver 
from graphene import Schema
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
