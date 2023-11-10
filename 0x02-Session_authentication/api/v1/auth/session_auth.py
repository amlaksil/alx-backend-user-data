#!/usr/bin/env python3
"""
This module contains a SessionAuth class for implementing
session-based authentication.
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import Optional
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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieve a User ID based on a Session ID.

        Args:
            session_id (str): The session ID for which to retrieve the user ID.

        Returns:
            str: The user ID associated with the session ID.

        Raises:
            None.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request: Optional[object] = None) -> Optional[User]:
        """
        Return a User instance based on a cookie value.

        Args:
            request (object): The request object containing the cookie value.

        Returns:
            Optional[User]: The User instance associated with the cookie value.

        Raises:
            None.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None

        return User.get(user_id)
