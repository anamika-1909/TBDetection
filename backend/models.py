from flask_sqlalchemy import SQLAlchemy
from uuid import uuid4
import datetime

db = SQLAlchemy()

def get_uuid():
    return uuid4().hex

class Patient(db.Model):
    __tablename__ = "patient"
    id = db.Column(db.String(32), primary_key=True, unique=True, default=get_uuid)
    email = db.Column(db.String(345), unique=True)
    password = db.Column(db.Text, nullable=False)

class Medical(db.Model):
    __tablename__ = "medical"
    id = db.Column(db.String(32), primary_key=True, unique=True)
    heartrate = db.Column(db.Integer, unique=False, default=60)
    bloodpressure = db.Column(db.Integer, unique=False, default=120) #systolic
    tbhistory = db.relationship('TBHistory', backref='patient')


class TBHistory(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, default=get_uuid)
    tbval = db.Column(db.Integer, unique=False, default=0) #percentage
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow) 
    patient_id = db.Column(db.String(32), db.ForeignKey('medical.id'))
