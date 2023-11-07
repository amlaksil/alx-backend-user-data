#!/usr/bin/env python3

"""
This module provides `BasicAuth` class, which extends the `Auth` class
and provides methods for basic authentication.
"""
from api.v1.auth.auth import Auth
import base64


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
        except base64.binascii.Error:
            return None
