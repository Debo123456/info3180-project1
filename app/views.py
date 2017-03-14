"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash, jsonify
from forms import LoginForm, UploadForm
from models import UserProfile, Profiles, ProfileSchema
from werkzeug.utils import secure_filename
from datetime import datetime


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')
 
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    
@app.route('/profile/', methods=["GET", "POST"])
def addProfile():
    form = UploadForm()
    if request.method == "POST" and form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        age = form.age.data
        gender = form.gender.data
        biography = form.biography.data
            
        image = form.image.data
        
        file_folder = app.config['UPLOAD_FOLDER']
        
        if image.filename == '':
            flash('No selected file', 'warning')
            return redirect(request.url)
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(file_folder, filename))
            profile = Profiles(first_name = firstname, last_name = lastname, username = username, age = age, gender = gender, image = filename, biography = biography, created_on = datetime.now())
            db.session.add(profile)
            db.session.commit()
            flash('Upload succesful', 'success')
            return redirect(request.url)
        else:
            flash('It looks like something went wrong', 'warning')
            return redirect(request.url)
    
    """Render the add-profile page."""
    return render_template('addprofile.html', form = form)
    
@app.route('/profile/<int:userid>', methods = ['POST', 'GET'])
def viewProfile(userid):
    profile = Profiles.query.filter_by(id=userid).first()
    
    if profile:
        if request.method == "POST":
            profile_schema = ProfileSchema()
            result = profile_schema.dump(profile)
            return jsonify( result.data )
        return render_template('profile.html', profile = profile, file_folder = app.config['UPLOAD_FOLDER'])
        
    flash('Profile not found', 'warning')
    return redirect(url_for('home'))
  
  
    
@app.route('/profiles/', methods = ['POST', 'GET'])
def profiles():
    profiles = Profiles.query.all()
    if profiles is not None:
        if request.method == "POST":
            profile_schema = ProfileSchema(many = True, only=('username', 'id'))
            result = profile_schema.dump(profiles)
            return jsonify({ "users": result.data})
        return render_template('profiles.html', profiles = profiles)
    flash('No profiles found', 'warning')
    return redirect(url_for('home'))
    


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")
