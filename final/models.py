from app import db
from flask_login import UserMixin
from flask_wtf import FlaskForm

class User(UserMixin ,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    firstname = db.Column(db.String(1000))
    lastname = db.Column(db.String(1000))
    age = db.Column(db.Integer) 
    weight = db.Column(db.Integer) 
    bp = db.Column(db.Integer) 
    bs = db.Column(db.Integer) 
    cough= db.Column(db.Integer) 
    pasttb= db.Column(db.String(4)) 

class EditAccountForm(FlaskForm):
    firstname = db.Column(db.String(1000))
    lastname = db.Column(db.String(1000))
    age = db.Column(db.Integer) 
    weight = db.Column(db.Integer) 
    bp = db.Column(db.Integer) 
    bs = db.Column(db.Integer) 
    cough= db.Column(db.Integer) 
    pasttb= db.Column(db.String(4)) 


    

# class Vitals(UserMixin,db.Model):
    
