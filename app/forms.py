
from wsgiref.validate import validator
from flask_wtf import FlaskForm
from wtforms import StringField, FileField, IntegerField, FloatField, SelectField
from wtforms.validators import InputRequired, DataRequired
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.widgets import TextArea

image_types = ['jpg', 'png', 'jpeg', 'gif', 'svg', 'webp']

class PropertyForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    beds = IntegerField('No. of Bedrooms', validators=[InputRequired()])
    baths = IntegerField('No. of Bathrooms', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    price = FloatField('Price', validators=[InputRequired()])
    type_ = SelectField('Type', choices=[('1', 'House'), ('2', 'Apartment')], validators=[InputRequired()])
    description = StringField('Description', validators=[InputRequired()], widget=TextArea())
    photo = FileField('Photo', validators=[FileAllowed(image_types, 'Image only!'), FileRequired('File was empty!')])

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    message= StringField('Message', validators=[DataRequired()], widget=TextArea())