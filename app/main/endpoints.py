from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Artist, Album, Track
from app.schemas import ArtistSchema, AlbumSchema, UserSchema, TrackSchema, AlbumTrackSchema
from app.utils import paginate_query
from app.main import main

users_schema = UserSchema(many=True)
artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)
album_schema = AlbumSchema()
albums_schema = AlbumSchema(many=True)
track_schema = TrackSchema()
tracks_schema = TrackSchema(many=True)

@main.route('/artists', methods=['GET'])
@jwt_required
def get_artists():
    return paginate_query(Artist.query, artists_schema, 'main.get_artists')

@main.route('/artists/<int:id>', methods=['GET'])
@jwt_required
def get_artist(id):
    artist = Artist.query.get_or_404(id)
    return jsonify(artist_schema.dump(artist))

@main.route('/artists/<int:id>', methods=['DELETE'])
@jwt_required
def delete_artist(id):
    artist = Artist.query.get_or_404(id)
    db.session.delete(artist)
    db.session.commit()
    return jsonify({'message': 'artist deleted'})

@main.route('/artists/<int:id>/albums', methods=['GET'])
@jwt_required
def get_artist_albums(id):
    artist = Artist.query.get_or_404(id)
    schema = AlbumTrackSchema(many=True)
    return paginate_query(artist.albums, schema, 'main.get_artist_albums', id=id)

@main.route('/artists/<int:id>/followers', methods=['GET'])
@jwt_required
def get_followers(id):
    artist = Artist.query.get_or_404(id)
    return paginate_query(artist.followers, users_schema, 'main.get_followers', id=id)

@main.route('/albums', methods=['GET'])
@jwt_required
def get_albums():
    return paginate_query(Album.query, albums_schema, 'main.get_albums')

@main.route('/albums/<int:id>', methods=['GET'])
@jwt_required
def get_album(id):
    album = Album.query.get_or_404(id)
    return jsonify(album_schema.dump(album))

@main.route('/albums/<int:id>', methods=['DELETE'])
@jwt_required
def delete_album(id):
    album = Album.query.get_or_404(id)
    db.session.delete(album)
    db.session.commit()
    return jsonify({'message': 'album deleted'})

@main.route('/albums/<int:id>/tracks', methods=['GET'])
@jwt_required
def get_album_tracks(id):
    album = Album.query.get_or_404(id)
    return jsonify(tracks_schema.dump(album.tracks))

@main.route('/tracks', methods=['GET'])
@jwt_required
def get_all_tracks():
    return paginate_query(Track.query, tracks_schema, 'main.get_all_tracks')

@main.route('/tracks/<int:id>', methods=['GET'])
@jwt_required
def get_track(id):
    track = Track.query.get_or_404(id)
    return jsonify(track_schema.dump(track))