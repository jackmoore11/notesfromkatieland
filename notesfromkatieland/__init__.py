from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from notesfromkatieland.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
loginManager = LoginManager()
loginManager.login_view = 'users.login'
loginManager.login_message_category = 'info'
mail = Mail()

def createApp(configClass=Config):
    app = Flask(__name__)
    app.config.from_object(configClass)

    db.init_app(app)
    bcrypt.init_app(app)
    loginManager.init_app(app)
    mail.init_app(app)

    from notesfromkatieland.users.routes import users
    from notesfromkatieland.posts.routes import posts
    from notesfromkatieland.main.routes import main
    from notesfromkatieland.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app