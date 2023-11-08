#!/usr/bin/env python3

"""
This module provides `BasicAuth` class, which extends the `Auth` class
and provides methods for basic authentication.
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    BasicAuth class extends the `Auth` class and provides methods for basic
    authentication.
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        Extracts the base64-encoded authorization header value from the
        given authorization header.

        Args:
            authorization_header (str): The authorization header value.

        Returns:
            str: The base64-encoded authorization header value.

        Notes:
        - Returns None if `authorization_header` is None or not a string.
        - Returns None if the authorization method is not 'Basic'.
        - Otherwise, returns the base64-encoded authorization header value.
        """
        if authorization_header is None\
           or not isinstance(authorization_header, str):
            return None
        str_a = authorization_header.split(' ', 1)
        if str_a[0] != 'Basic':
            return None
        return str_a[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """
        Decodes the given base64-encoded authorization header value.

        Args:
            base64_authorization_header (str): The base64-encoded authorization
            header value.

        Returns:
            str: The decoded value as a UTF-8 string.

        Notes:
        - Returns None if `base64_authorization_header` is None or not a string
        - Returns None if `base64_authorization_header` is not a valid Base64
          string (raises a `binascii.Error`).
        - Otherwise, returns the decoded value as a UTF-8 string.
        """
        if base64_authorization_header is None\
           or not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts the username and password from the decoded base64-encoded
        authorization header.

        Args:
            decoded_base64_authorization_header (str): The decoded
            base64-encoded authorization header value.

        Returns:
            tuple: A tuple containing the username and password extracted
            from the decoded authorization header.

        Notes:
        - Returns (None, None) if `decoded_base64_authorization_header` is
          None or not a string.
        - Returns (None, None) if the decoded authorization header does not
          contain a ':' character.
        - Otherwise, returns a tuple containingthe extracted username and
          password.
        """

        if decoded_base64_authorization_header is None\
           or not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        user_credentials = decoded_base64_authorization_header.split(':')
        return user_credentials[0], user_credentials[1]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """
        Returns the User instance based on the provided email and password.

        Args:
            user_email (str): The email of the user.
            user_pwd (str): The password of the user.

        Returns:
            TypeVar('User'): The User instance if the email and password are
            valid.
            None: If any of the following conditions are met:
                - `user_email` is None or not a string.
                - `user_pwd` is None or not a string.
                - The database (file) does n't contain any User instance with
                  an email equal to `user_email`.
                - `user_pwd` is not the password of the User instance found.
        """
        if user_email is None or user_pwd is None:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})
        if not users:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request
        """

        if request is None:
            return None

        auth_header = self.authorization_header(request)
        base64_auth_header = \
            self.extract_base64_authorization_header(auth_header)
        decoded_auth_header = \
            self.decode_base64_authorization_header(base64_auth_header)
        user_credentials = self.extract_user_credentials(decoded_auth_header)

        if user_credentials:
            email, password = user_credentials
            return self.user_object_from_credentials(email, password)

        return None
