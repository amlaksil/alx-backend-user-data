#!/usr/bin/env python3
"""
This module provides the `Auth` class, which serves as a template
for all authentication systems.
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class serves as a template for all authentication systems.
    """

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
