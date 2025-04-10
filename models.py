from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    
    # Relationships
    sent_parcels = db.relationship('Parcel', backref='sender', foreign_keys='Parcel.sender_id')
    received_parcels = db.relationship('Parcel', backref='recipient', foreign_keys='Parcel.recipient_id')

class Parcel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tracking_number = db.Column(db.String(8), unique=True, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    weight = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Foreign Keys
    sender_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    courier_id = db.Column(db.Integer, db.ForeignKey('courier.id'), nullable=True)
    
    # Relationships
    tracking_updates = db.relationship('TrackingUpdate', backref='parcel', lazy='dynamic')

class Courier(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='available')
    
    # Relationship
    parcels = db.relationship('Parcel', backref='courier')

class TrackingUpdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey('parcel.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)