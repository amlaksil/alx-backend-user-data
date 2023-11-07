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
            bool: True if authentication is required, False otherwise.

        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the Flask request object.

        Args:
            request (object): The Flask request object. (optional)

        Returns:
            str: The authorization header value.
        """
        return None

    def current_user(self, requests=None) -> TypeVar('user'):
        """
        Retrieves the current user from the Flask request object.

        Args:
            request (object): The Flask request object. (optional)

        Returns:
            TypeVar('User'): The current user.

        """
        return None
