#!/usr/bin/env python3

"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import inspect
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)

        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
           - email (str): The email of the user.
           - hashed_password (str): The hashed password of the user.

        Returns:
            - User: The created User object.
        """
        user = User(email=email, hashed_password=hashed_password)

        # Add the user to the session and commit.
        self._session.add(user)
        self._session.commit()

        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database based on the provided filters.

        Args:
            - **kwargs: Arbitrary keyword arguments representing the filters.

        Returns:
            - User: The first matching User object.

        Raises:
            - NoResultFound: If no user is found based on the provided filters.
            - InvalidRequestError: If wrong query argument are passed.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()

            if user is None:
                raise NoResultFound
        except InvalidRequestError as e:
            raise e
        return user

    def update_user(self, user_id: int, **kwargs):
        """
        Updates user data based on their id.

        Args:
            - user_id (int): User Id.
            - **kwargs (dict): Arbitrary keyword arguments represents the
            user filed to be updated.

        Returns:
            - None: If everything works as expected.

        Raises:
            - ValueError: If an argument that does not correspond to a user
            attribute is passed.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                user.key = value
                self._session.commit()
            else:
                raise ValueError
        return None
