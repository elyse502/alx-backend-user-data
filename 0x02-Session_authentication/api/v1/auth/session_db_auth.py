#!/usr/bin/env python3
""" Python Module """
from .session_exp_auth import SessionExpAuth
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    Definition of SessionDBAuth class that persists session data
    in a database
    """

    def create_session(self, user_id=None):
        """
        Create a Session ID for a user_id
        Args:
           user_id (str): user id
        """
        # Doesn’t return a Session ID and don’t create any UserSession
        # Record in DB if user_id = None
        if user_id is None or not isinstance(user_id, str):
            return None

        try:
            session_id = super().create_session(user_id)
            new_user_session = UserSession()
            new_user_session.user_id = user_id
            new_user_session.session_id = session_id
            new_user_session.save()
            return session_id
        except Exception as e:
            print("Error creating session:", e)
            return None

    def user_id_for_session_id(self, session_id=None):
        """ Returns a user ID based on a session ID
        Args:
            session_id (str): session ID
        Return:
            user id or None if session_id is None or not a string
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        try:
            user_session = UserSession.search({'session_id': session_id})
            if not user_session:
                return None
            user_json = user_session[0].to_json()

            if self.session_duration <= 0:
                return user_json.get('user_id')
            created_at = datetime.fromisoformat(user_json.get('created_at'))
            expiration_time = created_at + timedelta(
                seconds=self.session_duration)
            if expiration_time < datetime.now():
                return None
            return user_json.get('user_id')
        except Exception as e:
            print("Error retrieving user ID:", e)
            return None

    def destroy_session(self, request=None):
        """ Destroy a UserSession instance based on a
        Session ID from a request cookie
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False

        try:
            user_session = UserSession.search({'session_id': session_id})
            if not user_session:
                return False
            user_session[0].remove()
            return True
        except Exception as e:
            print("Error destroying session:", e)
            return False
