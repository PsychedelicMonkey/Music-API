from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

followers = db.Table('followers',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'))
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    followed = db.relationship('Artist', secondary=followers, lazy='dynamic',
        backref=db.backref('followers', lazy='dynamic'))

    def __repr__(self):
        return f'<User: {self.username}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def follow(self, artist):
        if not self.is_following(artist):
            self.followed.append(artist)

    def unfollow(self, artist):
        if self.is_following(artist):
            self.followed.remove(artist)

    def is_following(self, artist):
        return self.followed.filter(followers.c.artist_id == artist.id).count() > 0

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

    tracks = db.relationship('Track', backref='album', lazy='dynamic')

    def __repr__(self):
        return f'<Album: {self.name}, Artist: {self.artist.name}>'

class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_no = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'))
    runtime = db.Column(db.DateTime)
    released = db.Column(db.DateTime)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Track: {self.name}, Album: {self.album.name}>'