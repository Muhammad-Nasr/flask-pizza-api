from flask import Flask
from flask_restx import Api
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    authorizations={
        "Bearer Auth":{
            'type':"apiKey",
            'in':'header',
            'name':"Authorization",
            'description':"Add a JWT with ** Bearer &lt;JWT&gt; to authorize"
        }
    }

    api=Api(app,
        title="Pizza Delivery API",
        description="A REST API for a Pizza Delievry service",
        authorizations=authorizations,
        security="Bearer Auth",
        prefix="/doc"
    )
    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    

    api.add_namespace(auth, path='/auth')
    api.add_namespace(order, path='/orders')

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db':db,
            'User':User,
            'Order':Order,
        }

    
    return app


from .auth.views import auth
from .orders.views import order
from .models.models import User, Order 

