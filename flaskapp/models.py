from datetime import datetime
from flaskapp import app, db, login_manager
from flask_login import UserMixin
import flask_whooshalchemy as whoo

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    business = db.relationship("Business", backref="owner", lazy=True)
    review = db.relationship("Review", backref="author", lazy=True)

    def __repr__(self):
        return f"Username : {self.username} Email : {self.email} Location : {self.location}"

class Business(db.Model):
    __searchable__ = ['category']
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(100), unique=True, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    business_owner = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    review = db.relationship("Review", backref="business", lazy=True)

    def __repr__(self):
        return f"Business name : {self.business_name} Category : {self.category} Location : {self.location} Email : {self.email} Phone no. : {self.phone}"

whoo.whoosh_index(app, Business)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    posted_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    posted_for = db.Column(db.Integer, db.ForeignKey("business.id"), nullable=False)

    def __repr__(self):
        return f"Title : {self.title} Posted by : {self.posted_by} For : {self.posted_for} On : {self.date_posted}"
    

