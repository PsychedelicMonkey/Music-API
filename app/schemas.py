from marshmallow import post_load, fields
from app import ma
from app.models import User, Artist, Album

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = ma.auto_field(dump_only=True)
    username = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field(load_only=True, required=False)
    created = ma.auto_field(dump_only=True)

    _links = ma.Hyperlinks({
        'self': ma.URLFor('user.get_user', values=dict(id="<id>")),
    })

    @post_load
    def hash_password(self, data, **kwargs):
        if 'password' in data:
            user = User(**data)
            user.set_password(data['password'])
            data['password'] = user.password
        return data

class ArtistSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Artist

    albums_count = fields.Function(lambda obj: obj.albums.count())

    _links = ma.Hyperlinks({
        'self': ma.URLFor('main.get_artist', values=dict(id="<id>")),
        'albums': ma.URLFor('main.get_artist_albums', values=dict(id="<id>")),
    })

class AlbumSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Album

    _links = ma.Hyperlinks({
        'self': ma.URLFor('main.get_album', values=dict(id="<id>")),
    })