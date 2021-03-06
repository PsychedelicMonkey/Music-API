from marshmallow import post_load, fields
from app import ma
from app.models import User, Artist, Album, Track

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field(load_only=True, required=False)
    created = ma.auto_field(dump_only=True)

    followed_count = fields.Function(lambda obj: obj.followed.count())

    _links = ma.Hyperlinks({
        'self': ma.URLFor('user.get_user', values=dict(id="<id>")),
        'followed': ma.URLFor('user.get_followed', values=dict(id="<id>")),
    })

    @post_load
    def hash_password(self, data, **kwargs):
        if 'password' in data:
            user = User(**data)
            user.set_password(data['password'])
            data['password'] = user.password
        return data

class TrackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Track

    album = fields.Function(lambda obj: obj.album.name)

class AlbumSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Album

    track_count = fields.Function(lambda obj: obj.tracks.count())

    _links = ma.Hyperlinks({
        'self': ma.URLFor('main.get_album', values=dict(id="<id>")),
    })

class AlbumTrackSchema(AlbumSchema):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    tracks = fields.Nested(TrackSchema(only=('track_no', 'name',), many=True))

class ArtistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Artist

    albums_count = fields.Function(lambda obj: obj.albums.count())
    followers_count = fields.Function(lambda obj: obj.followers.count())

    _links = ma.Hyperlinks({
        'self': ma.URLFor('main.get_artist', values=dict(id="<id>")),
        'albums': ma.URLFor('main.get_artist_albums', values=dict(id="<id>")),
        'followers': ma.URLFor('main.get_followers', values=dict(id="<id>")),
    })