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