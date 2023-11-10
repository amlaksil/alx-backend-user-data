#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.auth.auth import Auth
from api.v1.auth.session_auth import SessionAuth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None
auth_type = getenv('AUTH_TYPE')
if auth_type:
    if auth_type == 'basic_auth':
        auth = BasicAuth()
    elif auth_type == 'session_auth':
        auth = SessionAuth()
    else:
        auth = Auth()


@app.errorhandler(401)
def handle_unauthorized_error(error) -> str:
    """
    Handles the 401 Unauthorized error.

    Args:
            error (Exception): The exception object representing the error.

    Returns:
            str: JSON-encoded string containing the error message.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def handle_forbidden_error(error) -> str:
    """
    Handle the 403 resource not allowed to access error.

    Args:
            error (Exception): The exception object representing the error.

        Returns:
    str: JSON-encoded string containing the error message.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.before_request
def before_request():
    """
    Flask before_request decorator that performs authentication checks.

    Notes:
        - The `auth` object is assumed to be an instance of the `Auth` class.
    """
    if auth:
        request.current_user = auth.current_user(request)
        path = request.path
        paths = ['/api/v1/status/',
                 '/api/v1/unauthorized/', '/api/v1/forbidden/',
                 '/api/v1/auth_session/login/']
        if auth.require_auth(path, paths):
            if auth.authorization_header(request) is None and\
               auth.session_cookie(request) is None:
                abort(401)
            if auth.current_user(request) is None:
                abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
