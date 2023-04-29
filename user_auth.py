from datetime import datetime, timedelta
from graphene import String,Mutation
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import jwt
from flask import request, jsonify
from models import User, Post


# Create an engine and sessionmaker for the database
engine = create_engine("mysql://root:root@localhost:3306/blogpost")
Session = sessionmaker(bind=engine)
session = Session()

SECRET_KEY = 'shyftlabs'

class Login(Mutation):
    class Arguments:
        username = String(required=True)
        password = String(required=True)

    token = String()

    def mutate(username, password):
        user = session.query(User).filter_by(username=username).first()
        if password == user.password:
            payload = {
                'username': str(user.username),
                'exp': datetime.utcnow() + timedelta(days=1)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        else:
            print("no match")

        return jsonify({"jwt_token": token})


def validate_user(token):
    if token:
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            username = data['username']
            expiry = data['exp']
            if expiry > int(datetime.utcnow().timestamp()):
                session = Session()
                user = session.query(User).filter_by(username=username).first()
                return user.id
            else:
                pass
        except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError):
            pass
    return None
