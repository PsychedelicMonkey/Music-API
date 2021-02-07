from flask import jsonify
from app.models import Artist, Album
from app.schemas import ArtistSchema, AlbumSchema, UserSchema
from app.utils import paginate_query
from app.main import main

users_schema = UserSchema(many=True)
artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)
album_schema = AlbumSchema()
albums_schema = AlbumSchema(many=True)

@main.route('/artists', methods=['GET'])
def get_artists():
    return paginate_query(Artist.query, artists_schema, 'main.get_artists')

@main.route('/artists/<int:id>', methods=['GET'])
def get_artist(id):
    artist = Artist.query.get_or_404(id)
    return jsonify(artist_schema.dump(artist))

@main.route('/artists/<int:id>/albums', methods=['GET'])
def get_artist_albums(id):
    artist = Artist.query.get_or_404(id)
    return paginate_query(artist.albums, albums_schema, 'main.get_artist_albums', id=id)

@main.route('/artists/<int:id>/followers', methods=['GET'])
def get_followers(id):
    artist = Artist.query.get_or_404(id)
    return paginate_query(artist.followers, users_schema, 'main.get_followers', id=id)

@main.route('/albums', methods=['GET'])
def get_albums():
    return paginate_query(Album.query, albums_schema, 'main.get_albums')

@main.route('/albums/<int:id>', methods=['GET'])
def get_album(id):
    album = Album.query.get_or_404(id)
    return jsonify(album_schema.dump(album))