#!/usr/bin/env python3
"""
This module contains a function called hash_password
that hashes the provided password using bcrypt with
a ranomly generated salt.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes the provided password using bcrypt with a randomly generated salt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The salted and hashed password as a byte string.

    """
    # Generate a random salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates if the provided password matches the given hashed
        password using bcrypt.

    Args:
        hashed_password (bytes): The hashed password to compare against.
        password (str): The password to be validated.

    Returns:
        bool: True if the password matches the hashed password,
                False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
