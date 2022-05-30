from hmac import new
from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from api.models.models import User, Order
from api import db
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import (create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity)



auth = Namespace('auth', description='a namespace for authentication')



signup_model=auth.model(
    'SignUp',{
        'id':fields.Integer(),
        'username':fields.String(required=True,description="A username"),
        'email':fields.String(required=True,description="An email"),
        'password':fields.String(required=True,description="A password"),
    }
)


user_signup_model=auth.model(
    'User',{
        'id':fields.Integer(),
        'username':fields.String(required=True,description="A username"),
        'email':fields.String(required=True,description="An email"),
        'password_hash':fields.String(required=True,description="A password"),
        'is_active':fields.Boolean(description="This shows that User is active"),
        'is_staff':fields.Boolean(description="This shows of use is staff")
    }

)

user_login_model = auth.model(
    'Login', {'username': fields.String(required=True, description='Username'),
            'password': fields.String(required=True, description='password')}
)


@auth.route('/signup')
class SignUp(Resource):
    @auth.expect(signup_model)
    @auth.marshal_with(user_signup_model)
    def post(self):
        """
        create a new user
        """
        data = request.get_json()
        new_user=User(
                username=data.get('username'),
                email=data.get('email'),
                password_hash=generate_password_hash(data.get('password'))
            )
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201


@auth.route('/login')
class Login(Resource):
    @auth.expect(user_login_model)
    def post(self):
        """
        log in user
        """
        input_data = request.get_json()
        user = User.query.filter_by(username=input_data.get('username')).first()
        if user and check_password_hash(user.password_hash, input_data.get('password')):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            
            return jsonify({  
                'acess_token': access_token,
            'refresh_token': refresh_token,
             'username': user.username
             })

    
    @auth.route('/refresh')
    class RefreshToken(Resource):
        @jwt_required(refresh=True)
        def post(self):
            username = get_jwt_identity()
            
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'username': username
            })
