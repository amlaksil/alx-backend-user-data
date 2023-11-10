#!/usr/bin/env python3
"""
This module provides the `Auth` class, which serves as a template
for all authentication systems.
"""
from flask import request
from typing import List, TypeVar, Optional
import os


class Auth:
    """
    Auth class serves as a template for all authentication systems.
    """

    def __init__(self):
        """
        Initializes an instance of the AuthHandler class.

        The constructor retrieves the session name from the SESSION_NAME
        environment variable. If the environment variable is not defined, it
        assigns a default session name of '_my_session_id'.
        """
        self.session_name = os.environ.get('SESSION_NAME', '_my_session_id')

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether authentication is required for the given path.

        Args:
            path (str): The path to check for authentication requirement.
            excluded_paths (List[str]): A list of paths excluded from
            authentication requirement.

        Returns:
            bool: Returns False if `path` is in `excluded_paths`, taking
            into account the slash tolerance. Otherwise True.
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        path_t = (path if '/' == path[len(path) - 1] else path + '/')
        for path in excluded_paths:
            if path[len(path) - 1] == '*':
                sub_path = path[:len(path) - 1]
                if sub_path in path_t:
                    return False
        if path_t in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the Flask request object.

        Args:
            request (object): The Flask request object. (optional)

        Returns:
            str: The authorization header value.
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, requests=None) -> TypeVar('user'):
        """
        Retrieves the current user from the Flask request object.

        Args:
            request (object): The Flask request object. (optional)

        Returns:
            TypeVar('User'): The current user.

        """
        return None

    def session_cookie(
            self, request: Optional[object] = None) -> Optional[str]:
        """
        Returns the value of the session cookie from a given request.

        Args:
            request (object, optional): The request object containing cookies.
            Defaults to None.

        Returns:
            str or None: The value of the session cookie if found, or
        None if the request is None or the cookie is not present.
        """
        if request is None:
            return None

        return request.cookies.get(self.session_name, None)
