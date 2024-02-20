from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db=SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    users_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    users_fullname = db.Column(db.String(70), nullable=False)
    users_email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    time_sent = db.Column(db.DateTime(), default=datetime.utcnow)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    admin_username = db.Column(db.String(50), unique=True, nullable=False)
    admin_password = db.Column(db.String(100), nullable=False)

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    github_url = db.Column(db.String(100), nullable=False)
    live_url = db.Column(db.String(100), nullable=True)
    port_desc = db.Column(db.Text, nullable=False)
    site_pic = db.Column(db.String(225), nullable=True)

class SocialMedia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x_url = db.Column(db.String(255), nullable=True)
    github_url = db.Column(db.String(255), nullable=True)
    linkedin_url = db.Column(db.String(255), nullable=True)
    instagram = db.Column(db.String(255), nullable=True)
    thread = db.Column(db.String(255), nullable=True)
