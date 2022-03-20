from . import db
#from werkzeug.security import generate_password_hash




class Property(db.Model):
    # You can use this to change the table name. The default convention is to use
    # the class name. In this case a class name of UserProfile would create a
    # user_profile (singular) table, but if we specify __tablename__ we can change it
    # to `user_profiles` (plural) or some other name.
    __tablename__ = 'property_profiles'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    beds = db.Column(db.Integer)
    baths = db.Column(db.Integer)
    location = db.Column(db.String(100))
    price = db.Column(db.Float)
    type_ = db.Column(db.Integer)
    description = db.Column(db.Text)
    img = db.Column(db.Text)

    def __init__(self, title, beds, baths, location, price, description, type_, img):
        self.title = title
        self.beds = beds
        self.baths = baths
        self.location = location
        self.price = price
        self.type_ = type_
        self.description = description
        self.img = img
        

    def get_id(self):
        return str(self.id)  # python 3 support

    def __repr__(self):
        return '<House/Apartment %r>' % (self.title)


"""

if alembic error hsoes follow the example below when trying to do a flask db migrate or upgrade

I encountered this problem and solved it by importing my models at env.py in the migrations folder right after the following comments

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

from app.models import Student, Tutor


"""