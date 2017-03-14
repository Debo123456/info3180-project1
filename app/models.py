from . import db
from marshmallow import Schema, fields


##### MODELS #####

class UserProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(255))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
        
        
class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    username = db.Column(db.String(80))
    age = db.Column(db.String(80))
    gender = db.Column(db.String(80))
    image = db.Column(db.String(80))
    biography = db.Column(db.String(200))
    created_on = db.Column(db.DateTime)
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
            
            
##### SCHEMAS #####

class ProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    age = fields.Str()
    image = fields.Str()
    gender = fields.Str()
    biography = fields.Str()
    formatted_name = fields.Method("format_name", dump_only=True)
    
    def format_name(self, profile):
        return "{}, {}".format(profile.lastname, profile.firstname)

   

    
