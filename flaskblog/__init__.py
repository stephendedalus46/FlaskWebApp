from flask import Flask  # import Flask class from flask framework
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail  # enable to send emails to users
from flaskblog.config import Config  # file with all configurations created by us, env var...


db = SQLAlchemy()  # instance of DB, since create_app func, no app arg needed
bcrypt = Bcrypt()  # instance of Bcrypt class that we use to hash passwords, since create_app func, no app arg needed
login_manager = LoginManager()  # instance of flask class to handle login, since create_app func, no app arg needed
login_manager.login_view = 'users.login'  # 'login' is function name of login route, it's for @login_required decorator
login_manager.login_message_category = 'info'  # info is bootstrap class

mail = Mail()  # initializing extension, since create_app func, no app arg needed


def create_app(config_class=Config):
    app = Flask(__name__)  # __name__ is name of the module (can be equal to __main__) this is for flask to know everything
    app.config.from_object(Config)  # connecting to out config.py

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    #BLUEPRINTS

    #  from flaskblog import routes, doesn't work after Blueprint cleaning
    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
