from . import db
from datetime import datetime

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(200), nullable=False)
    solo_level = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    mcqs = db.relationship('MCQ', backref='request', lazy=True)

class MCQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), nullable=False)
    question_text = db.Column(db.String(500), nullable=False)
    options = db.relationship('Option', backref='mcq', lazy=True)

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mcq_id = db.Column(db.Integer, db.ForeignKey('mcq.id'), nullable=False)
    option_text = db.Column(db.String(200), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
