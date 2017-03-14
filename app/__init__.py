from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "change this to be a more random key"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://user:password@localhost/project1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

db = SQLAlchemy(app)

UPLOAD_FOLDER = './app/static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config.from_object(__name__)
from app import views
