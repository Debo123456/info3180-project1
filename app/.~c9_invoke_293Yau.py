"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, current_user, login_required
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
    
    if profile is not None:
        if request.method == "POST" and request.headers['Content-Type'] == "application/json":
            profile_schema = ProfileSchema()
            result = profile_schema.dump(profile)
            return jsonify({'Profile': result})
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
            return jsonify(result)
        return render_template('profiles.html', profiles = profiles)
    flash('No profiles found', 'warning')
    return redirect(url_for('home'))



@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        # change this to actually validate the entire form submission
        # and not just one field
        if form.username.data and form.username.data:
            # Get the username and password values from the form.
            username = form.username.data
            password = form.password.data

            # using your model, query database for a user based on the username
            # and password submitted
            user = UserProfile.query.filter_by(username=username, password=password).first()
            
            # store the result of that query to a `user` variable so it can be
            # passed to the login_user() method.
            
            if user is not None:
                # get user id, load into session
                login_user(user)

                # remember to flash a message to the user
                flash('Logged in successfully.', 'success')
                return redirect(url_for("secure_page")) # they should be redirected to a secure-page route instead
            else:
                flash('Username or Password is incorrect.', 'danger')
                
    return render_template("login.html", form=form)
    
    
@app.route('/secure-page')
@login_required
def secure_page():
    """Render the website's secure page"""
    return render_template('secure_page.html')
    
    
    
@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        
        flash('You have been logged out', 'warning')
        logout_user()
        return redirect(url_for("home"))
    
    return redirect(url_for("home"))
    

# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))
    


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
