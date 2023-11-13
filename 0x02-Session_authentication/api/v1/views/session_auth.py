#!/usr/bin/env python3

"""
This module handles the login process using session authentication.
"""
from api.v1.views import app_views
from flask import abort, jsonify, request, session
from os import getenv
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    Handle the login process using session authentication.

    Returns:
        Response: JSON response with user data or error message.
    """
    user_email = request.form.get('email')
    user_password = request.form.get('password')

    if not user_email:
        return jsonify({"error": "email missing"}), 400

    if not user_password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({"email": user_email})
    if not users or users == []:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(user_password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            user_data = user.to_json()
            response = jsonify(user_data)
            response.set_cookie(getenv('SESSION_NAME'), session_id)
            return response

    return jsonify({"error": "wrong password"}), 401
