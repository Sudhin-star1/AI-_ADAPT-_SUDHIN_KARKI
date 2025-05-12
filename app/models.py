from . import db
from datetime import datetime

# Creating database models for the whole task to record user provided input as well as formatted output.

# This model represents the request made by the user to create a MCQ
class Request(db.Model):
    # Unique ID for the request
    id = db.Column(db.Integer, primary_key=True) 
    topic = db.Column(db.String(200), nullable=False)
    solo_level = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    mcqs = db.relationship('MCQ', backref='request', lazy=True)

# This model represents a single MCQ generated from a request
class MCQ(db.Model):
    # Unique id for MCQ
    id = db.Column(db.Integer, primary_key=True)
    # Link to parent request
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    question_text = db.Column(db.String(500), nullable=False)
    options = db.relationship('Option', backref='mcq', lazy=True)

# This model represents an answer option for an MCQ
class Option(db.Model):
    # Unique ID for the option
    id = db.Column(db.Integer, primary_key=True)
    # Link to parent MCQ
    mcq_id = db.Column(db.Integer, db.ForeignKey('mcq.id'), nullable=False)
    option_text = db.Column(db.String(200), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
