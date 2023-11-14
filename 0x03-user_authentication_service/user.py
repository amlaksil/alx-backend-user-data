#!/usr/bin/env python3

"""
Module: user

This module defines the SQLAlchemy model `User` for the `users` table.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    SQLAlchemy model representing a user in the `users` table.

    Attributes:
        - id (int): The integer primary key of the user.
        - email (str): The non-nullable email of the user.
        - hashed_password (str): The non-nullable hashed password of the user.
        - session_id (str): The nullable session ID of the user.
        - reset_token (str): The nullable reset token of the user.

    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
