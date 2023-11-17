#!/usr/bin/env python3

from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

AUTH = Auth()

app = Flask(__name__)


@app.route('/')
def message() -> str:
    """Returns a JSON payload"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """
    Register a user with their email and password.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
    Creates a new session for the user, store it the session ID
    as a cookie with key `session_id` on the response and return
    a JSON payload of the form.

    Raises:
        401 Unauthorized: Raises a 401 error to indicate unauthorized access.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie('session_id', session_id)
        return response

    abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """
    Logout route to destroy a user session.

    The request is expected to contain the session ID as a cookie
    with the key "session_id". If the user exists with the requested
    session ID, the session is destroyed, and the user is redirected
    to the homepage.

    If the user does not exist, a "Forbidden" response with HTTP status
    403 is returned.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile():
    """
    Profile route to find the user based on session_id.
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """
    Endpoint to generate a reset password token for a given email.

    Args:
        email (str): The email of the user requesting the password reset.

    Returns:
        - JSON response containing the email and reset_token if successful.
        - HTTP status code 200 (OK) on success.
        - HTTP status code 403 (Forbidden) if the email does not exist.
    """
    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password() -> str:
    """
    Endpoint to update the password using a reset token.

    Args:
        email (str): The email of the user requesting the password update.
        reset_token (str): The reset token received by the user.
        new_password (str): The new password to be set.

    Returns:
        JSON response containing the email and a success
        message if the password update is successful.
        HTTP status code 403 (Forbidden) if the password update fails.

    Raises:
        Exception: If an error occurs during the password update process.

    """
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
