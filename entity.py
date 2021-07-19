from extend import db
from datetime import datetime


class Event(db.Model):
    __tablename__ = 'event_info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_type=db.Column(db.Integer,nullable=True)
    event_date=db.Column(db.DateTime,default=datetime.now,nullable=True)
    event_location=db.Column(db.String(200),nullable=True)
    event_desc=db.Column(db.String(200),nullable=True)
    oldperson_id=db.Column(db.Integer,nullable=True)
    # db.ForeignKey("user.id", ondelete='cascade')

