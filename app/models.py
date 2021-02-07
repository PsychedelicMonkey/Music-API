from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User: {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    albums = db.relationship('Album', backref='artist', lazy='dynamic')

    def __repr__(self):
        return f'<Artist: {self.name}>'

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'))
    released = db.Column(db.DateTime)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Album: {self.name}, Artist: {self.artist.name}>'