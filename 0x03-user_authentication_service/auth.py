#!/usr/bin/env python3
"""
This module contains a function `_hash_password` that
takes a password string arguments and returns bytes, `_generate_uuid`
that returns a string representation of UUID, and a class `Auth` to
interact with the authentication database .
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """
    Hashes a given string argument.

    Args:
            password (str): String argument.

    Returns:
            bytes: A hashed value of a given password in bytes format.
    """
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pwd


def _generate_uuid() -> str:
    """
    Returns a string representation of a new UUID.
    """
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a user if it is not already exists.

        Args:
            email (str): User email.
            password (str): User password.

        Returns:
            User (obj): A user object.

        Raises:
            ValueError: If a user already exists with the provided email.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd)

    def valid_login(self, email: str, password: str) -> bool:
        """
        Checks if the user uses a valid email and password.

        Args:
            email (str): User email.
            password (str): User password.

        Returns:
            Boolean: True if password matches otherwise False.
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_pwd = user.hashed_password

            if bcrypt.checkpw(password.encode('utf-8'), hashed_pwd):
                return True
            return False
        except (NoResultFound, InvalidRequestError):
            return False

    def create_session(self, email: str) -> str:
        """
        Finds the user corresponding to the email, generate a new UUID
        and stroe it in the database.

        Args:
            email (str): User email.

        Returns:
            str: User's session_id.
        """
        try:
            user = self._db.find_user_by(email=email)
            new_uuid = _generate_uuid()
            user.session_id = new_uuid
            self._db._session.commit()
            return new_uuid
        except NoResultFound:
            pass

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Gets the user based on the session_id.

        Args:
            session_id (str): Session id.

        Returns:
            User (obj): User object. If the session ID is None or no user is
            found, return None.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            pass

    def destroy_session(self, user_id: int) -> None:
        """
        Updates the corresponding user's session ID to None.

        Args:
            user_id (int): User ID.

        Returns:
            None
        """
        return self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate and retrieve a reset password token for the user with
        the provided email.

        Args:
            email (str): The email of the user for whom to generate the
            reset password token.

        Returns:
            str: The generated reset password token.

        Raises:
            ValueError: If no user is found with the provided email.
        """
        try:
            user = self._db.find_user_by(email=email)
            user.reset_token = _generate_uuid()
            return user.reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update the password for the user associated with the provided
        reset token.

        Args:
            reset_token (str): The reset token associated with the user.
            password (str): The new password to set for the user.

        Raises:
            ValueError: If no user is found with the provided reset token
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            user.hashed_password = _hash_password(password)
            user.reset_token = None
            return None
        except NoResultFound:
            raise ValueError
