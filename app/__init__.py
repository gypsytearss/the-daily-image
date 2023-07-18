import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()

load_dotenv()


def create_app() -> Flask:
    """
    Create and return the flask app.
    """

    template_dir = os.path.abspath('./templates')
    static_dir = os.path.abspath('./static')

    app = Flask(__name__,
                template_folder=template_dir,
                static_folder=static_dir)

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO")

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

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()