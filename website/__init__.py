from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database2.db"

def create_all():
    app = Flask(__name__) 

    app.config['SECRET_KEY'] = 'princess'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .api import api
    from .admin import admin

    with app.app_context():
        db.create_all()

    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(api, url_prefix='/')

    from .models import User, Admin
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        user = User.query.get(int(id))
        #if no user is gotten from the user table, the admin table is queried
        # if not user:
        #     user = Admin.query.get(int(id))
        return user
    


    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
