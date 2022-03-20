"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""
from fileinput import filename
import mimetypes
import os
from io import BytesIO
from app import app
from flask import render_template, request, redirect, url_for, flash, Response, send_file
from flask.helpers import send_from_directory
from werkzeug.utils import secure_filename
from app.forms import PropertyForm
from app.models import Property
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)


def get_uploaded_images():
    image_types = ['jpg', 'png', 'jpeg', 'gif', 'svg', 'webp']
    
    upload_dir = app.config.get('UPLOAD_FOLDER')
    uploads = sorted(os.listdir(upload_dir))

    #this is done to only show file types in image_types list
    cleaned = [img for img in uploads if any(sub in img for sub in image_types)]
    return cleaned

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
    return render_template('about.html', name="Raffique Muir")


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/properties')
def properties():
    """Render the website's cerate property page."""

    #files = get_uploaded_images()
    files = Property.query.all()
    return render_template('properties.html', files=files)

@app.route('/properties/<propertyid>')
def specific_property(propertyid):
    
    file = Property.query.filter_by(id=propertyid).first()
    return render_template('property.html', file=file)

@app.route('/properties/create', methods=["GET", "POST"])
def create():
    """Render the website's cerate property page."""

    form = PropertyForm()

    if request.method == "POST":
        if form.validate_on_submit():
            title = form.title.data
            beds = form.beds.data
            baths = form.baths.data
            location = form.location.data
            price = form.price.data
            type_ = form.type_.data
            description = form.description.data
            file = form.photo.data

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


            property = Property(title=title, beds=beds, baths=baths, location=location, price=price, type_=type_, description=description, img=filename)
            db.session.add(property)
            db.session.commit()

            flash('Successful added property!', 'danger')
            return redirect(url_for("properties"))  # they should be redirected to a secure-page route instead

    return render_template('create.html', form=form)


@app.route('/uploads/<filename>')
def get_image(filename):
    upload_dir =  os.path.join(os.getcwd(), app.config.get('UPLOAD_FOLDER'))
    return send_from_directory(upload_dir, filename,)



# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
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
