#!/usr/bin/env python3
""" Module of Index views
"""
from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """ GET /api/v1/status
    Return:
      - the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """ GET /api/v1/stats
    Return:
      - the number of each objects
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized', strict_slashes=False)
def unauthorized() -> None:
    """
    Handles unauthorized access to the API endpoint.

    Raises:
    401 Unauthorized: Raises a 401 error to indicate unauthorized access.

    Returns:
            None
    """
    abort(401)


@app_views.route('/forbidden', strict_slashes=False)
def forbidden() -> None:
    """
    Handle requests to the /forbidden endpoint.

    Raises:
            403: If the user is authenticated but not allowed to access
            the resource.

    Returns:
            None
    """
    abort(403)
