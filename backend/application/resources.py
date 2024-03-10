from flask_restful import Resource, Api, reqparse, fields, marshal
from flask_security import auth_token_required, current_user
from flask import jsonify, make_response
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_
from .sec import datastore
from .models import db, User, Role

api=Api(prefix='/api')

class login(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument('email', type=str, required=True)
        self.parser.add_argument('password', type=str, required=True)

    def post(self):
        args= self.parser.parse_args()
        email=args.get("email")    
        password=args.get("password")

        user=datastore.find_user(email=email)
        
        if not user:
            print('user does not exist')
            return make_response(jsonify({"message":"User doesn't exist!"}), 400)
        
        elif user and check_password_hash(user.password,password):
            token=user.get_auth_token()
            print("success!")
            return jsonify({
                            "token": token,
                             "email": user.email,
                             "username":user.username,
                             "role": user.roles[0].name      
                             })
        
        elif user.email=='admin@syncin.ac.in':
            return make_response(jsonify({"message":"Incorrect password"}), 400)
        else:
            return make_response(jsonify({"message":"Incorrect username or password"}), 400)

api.add_resource(login, '/login')

class register(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument('username', type=str, required=True)
        self.parser.add_argument('email', type=str, required=True)
        self.parser.add_argument('password', type=str, required=True)
        self.parser.add_argument('creator', type=bool, required=True)

    def post(self):
        args= self.parser.parse_args()
        password=args.get("password")
        uname=args.get("username")
        email=args.get("email")
        creator=args.get("creator")

        user=datastore.find_user(email=email)
        if (email=="admin@syncin.ac.in"):
             return make_response(jsonify({"message":"Enter a valid email!"}), 400)
        if user:
            return make_response(jsonify({"message":"Email already exists!"}), 400)
        
        
        r="creator" if creator else "user"
        #role = Role.query.filter_by(name=r).first()
        datastore.create_user(email=email,
                              password=generate_password_hash(password),
                              username=uname,
                              roles=[r],
                              active=1)
    
        db.session.commit()
        user=datastore.find_user(email=email)
        return jsonify({"userdata":{
                            "token": user.get_auth_token(),
                            "email": user.email,
                            "username":user.username,
                            "role": user.roles[0].name,
                            },
                        "message":"account created"})

api.add_resource(register, '/register')    

class authenticate(Resource):

    @auth_token_required
    def get(self):
        return jsonify({'authenticated': True})

        
api.add_resource(authenticate, '/authenticate') 


class retreive(Resource):
    
    @auth_token_required
    def get(self):
        return jsonify({"email": current_user.email,
                        "username":current_user.username,
                        "role": current_user.roles[0].name,
                        })
    
api.add_resource(retreive,'/retreive')    


        













