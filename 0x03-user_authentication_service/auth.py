#!/usr/bin/env python3
"""
Module auth
"""
from bcrypt import hashpw, gensalt, checkpw
from uuid import uuid4
from typing import Union

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Returns a salted hash of
    the input password
    """
    hashed_password = hashpw(password.encode('utf-8'), gensalt())

    return hashed_password


def _generate_uuid() -> str:
    """
    Returns string representation
    of a new UUID
    """
    uid = str(uuid4())
    return uid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a new user"""
        try:
            # Find the user with the given email
            user = self._db.find_user_by(email=email)
            if user:
                # If user already exists, throw error
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            # Add user to database
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ Validates credentials

        Args:
            email (str): _description_
            password (str): _description_

        Returns:
            Boolean: _description_
        """
        try:
            # Find the user with the given email
            user = self._db.find_user_by(email=email)
            return checkpw(
                    password.encode('utf-8'),
                    user.hashed_password
                    )
        except NoResultFound:
            return False
        # Check validity of password
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """
        Creates a session from a
        user and stores session id in
        database
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)

        return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """
        Finds a user using the session id
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """
        Removes user_id's session from
        database
        """
        if user_id is None:
            return None

        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
            return None
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ Generates a reset password token for a user

        Args:
            email (str): _description_

        Returns:
            str: _description_
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates a user's password

        Args:
            reset_token (str): _description_
            password (str): _description_
        """
        if reset_token is None or password is None:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(user.id,
                             hashed_password=hashed_password,
                             reset_token=None)
