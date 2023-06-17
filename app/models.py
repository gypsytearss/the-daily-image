from flask_login import UserMixin
from sqlalchemy.sql.functions import now
from . import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, db.Identity(start=10, cycle=True), primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    @property
    def initials(self):
        if not self.name:
            return "?"
        names = self.name.split()
        print(f"Names {names}")
        initials = names[0][0].upper()
        if len(names) > 1:
            initials += names[-1][0].upper()
        return initials

class Images(db.Model):
    uuid = db.Column(db.Uuid, primary_key=True)
    title = db.Column(db.String(1000))
    url = db.Column(db.String(1000))
    creator = db.Column(db.String(1000))
    license = db.Column(db.String(100))
    license_url = db.Column(db.String(1000))
    license_version = db.Column(db.String(100))
    thumbnail_url = db.Column(db.String(1000))

class UserImages(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), primary_key=True)
    image_uuid = db.Column(db.Uuid, db.ForeignKey(Images.uuid), primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=now())
    annotation = db.Column(db.String(10000))