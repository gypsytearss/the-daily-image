import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app() -> Flask:
    template_dir = os.path.abspath('./templates')
    static_dir = os.path.abspath('./static')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    app.config["SECRET_KEY"] = "my-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'user.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app