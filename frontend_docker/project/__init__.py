import os
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bcrypt = Bcrypt(app)  # password hashing

# set environmental variable to development or production class
app.config.from_object(os.environ['APP_MODE'])

# database connection
db = SQLAlchemy(app)

# import blueprints
from project.users.views import users_blueprint
from project.main.views import main_blueprint

# register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(main_blueprint)
