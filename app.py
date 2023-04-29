from flask import Flask,request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import resolver 
from user_auth import Login
from graphene import Schema
from flask_graphql import GraphQLView

app = Flask(__name__)
CORS(app)

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data['username']
    email = data['email']
    password = data['password']
    id = data["id"]
    resolver.Signup.mutate(username = username, password=password,email=email, id = id)
    response="User created"
    return response

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

# @app.route("/delete/id/<id>",methods=["Delete"])
# def deletepost(id):
#     data = request.get_json()
#     id = id
#     token = data["token"]
#     return resolver.DeletePost.mutate(id = id,token = token)

# schema = Schema(query = resolver.Query)

# @app.route('/blogpost',method=['POST'])
# def blogpost():
#     query = request.json.get('query')
#     variables = request.json.get('variables')
    
#     result = schema.execute(query, variable_values=variables)
    
#     return jsonify(result.data)


# query = ObjectType("Query")

# query.set_field("getqueries", resolver.Query)

# type_defs = load_schema_from_path("schema.graphql")
# schema = make_executable_schema(
#     type_defs, query, snake_case_fallback_resolvers
# )


# @app.route("/graphql", methods=["POST"])
# def graphql_server():
#     data = request.get_json()

#     success, result = graphql_sync(
#         schema,
#         data,
#         context_value=request,
#         debug=app.debug
#     )

#     status_code = 200 if success else 400
#     return jsonify(result), status_code

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=resolver.schema,
        graphiql=True
    ),
)
