from flask import jsonify, request, url_for
from app import db
from app.errors import bad_request
from app.models import User
from app.schemas import UserSchema, ArtistSchema
from app.utils import paginate_query
from app.user import user

user_schema = UserSchema()
users_schema = UserSchema(many=True)
artists_schema = ArtistSchema(many=True)

@user.route('/users', methods=['GET'])
def get_users():
    return paginate_query(User.query, users_schema, 'user.get_users')

@user.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user_schema.dump(user))

@user.route('/users/<int:id>/followed', methods=['GET'])
def get_followed(id):
    user = User.query.get_or_404(id)
    return paginate_query(user.followed, artists_schema, 'user.get_followed', id=id)

@user.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use another username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use another email address')
    user = user_schema.load(data)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user_schema.dump(user))
    response.status_code = 201
    response.headers['Location'] = url_for('user.get_user', id=user.id)
    return response

@user.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json() or {}
    if 'username' in data and data['username'] != user.username and User.query.filter_by(username=data['username']).first():
        return bad_request('please use another username')
    if 'email' in data and data['email'] != user.email and User.query.filter_by(email=data['email']).first():
        return bad_request('please use another email address')
    user_schema.load(data, instance=user)
    db.session.commit()
    return jsonify(user_schema.dump(user))