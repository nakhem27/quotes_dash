from flask import Flask
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.sql import func
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
import re

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "ajdflakdjfl"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quote_dash.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)