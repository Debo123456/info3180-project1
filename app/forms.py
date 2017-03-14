from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    
class UploadForm(FlaskForm):
    firstname = StringField('firstname', validators=[InputRequired()])
    lastname = StringField('lastname', validators=[InputRequired()])
    age = StringField('age', validators=[InputRequired()])
    gender = StringField('gender', validators=[InputRequired()])
    image = FileField('image', validators=[
            FileRequired(),
            FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
        ])
    biography = StringField('biography', validators=[InputRequired()])
    username = StringField('username', validators=[InputRequired()])
