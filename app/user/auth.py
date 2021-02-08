from flask import jsonify, request
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_refresh_token_required
from app.models import User
from app.errors import bad_request, unauthorized
from app.user import user

@user.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    if 'username' not in data or 'password' not in data:
        return bad_request('must include username and password fields')
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        return jsonify({
            'access': create_access_token(user.id),
            'refresh': create_refresh_token(user.id),
        })
    return unauthorized('invalid username or password')

@user.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    return jsonify({
        'access': create_access_token(identity=current_user),
    })