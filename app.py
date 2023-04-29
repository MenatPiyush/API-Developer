from flask import Flask,request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import resolver 
from graphene import Schema
from flask_graphql import GraphQLView

app = Flask(__name__)
CORS(app)

# @app.route("/signup", methods=["POST"])
# def signup():
#     data = request.get_json()
#     username = data['username']
#     email = data['email']
#     password = data['password']
#     id = data["id"]
#     resolver.Signup.mutate(username = username, password=password,email=email, id = id)
#     response="User created"
#     return response

@app.route("/login", methods=["GET"])
def login():
    data = request.get_json()
    print(data)
    username = data["username"]
    password = data["password"]
    return Login.mutate(username = username,password=password)
    
@app.route("/createpost",methods=["POST"])
def createpost():
    data = request.get_json()
    print(data)
    title = data["title"]
    content = data["content"]
    token = data["token"]
    return resolver.CreatePost.mutate(title = title,content = content,token = token)

@app.route("/posts" ,methods=["GET"])
def getposts():
    result = resolver.Query.resolve_posts()
    print(result)
    

@app.route("/update/id/<id>",methods=["POST"])
def updatepost(id):
    data = request.get_json()
    id = id
    title = data["title"]
    content = data["content"]
    token = data["token"]
    return resolver.UpdatePost.mutate(id = id,title = title,content = content,token = token)

@app.route("/delete/id/<id>",methods=["Delete"])
def deletepost(id):
    data = request.get_json()
    id = id
    token = data["token"]
    return resolver.DeletePost.mutate(id = id,token = token)

schema = Schema(query = resolver.Query)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=resolver.schema,
        graphiql=True
    ),
)
