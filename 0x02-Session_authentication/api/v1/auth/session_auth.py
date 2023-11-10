#!/usr/bin/env python3
"""
This module contains a SessionAuth class for implementing
session-based authentication.
"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """
    SessionAuth class for implementing session-based authentication.

    This class inherits from the Auth class and serves as the starting point
    for implementing a new authentication mechanism based on sessions.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Create a Session ID for a user_id.

        Args:
            user_id (str): The user ID for which to create a session.

        Returns:
            str: The generated session ID.

        Raises:
            None.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id
