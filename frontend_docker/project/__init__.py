import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bcrypt = Bcrypt(app)  # password hashing

# set environmental variable to development or production class
app.config.from_object(os.environ['APP_MODE'])

# database connection
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# import blueprints
from project.users.views import users_blueprint
from project.main.views import main_blueprint

# register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(main_blueprint)

from project.models import User

login_manager.login_view = "users.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
