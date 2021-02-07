from flask import request
from app import db
from app.errors import error_response
from app.main import main

def wants_json_response():
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']

@main.app_errorhandler(404)
def page_not_found(e):
    if wants_json_response():
        return error_response(404)
    return '404', 404

@main.app_errorhandler(500)
def unknown_error(e):
    db.session.rollback()
    if wants_json_response():
        return error_response(500)
    return '500', 500