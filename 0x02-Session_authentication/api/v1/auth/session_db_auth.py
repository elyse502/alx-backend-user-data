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
        try:
            # Doesn’t return a Session ID and don’t create any UserSession
            # Record in DB if user_id = None
            if user_id is None or not isinstance(user_id, str):
                return None

            session_id = super().create_session(user_id)
            new_user_session = UserSession()
            new_user_session.user_id = user_id
            new_user_session.session_id = session_id
            new_user_session.save()
            return session_id
        except Exception as e:
            print(f"An error occurred in create_session: {e}")
            return None

    def user_id_for_session_id(self, session_id=None):
        """ Returns a user ID based on a session ID
        Args:
            session_id (str): session ID
        Return:
            user id or None if session_id is None or not a string
        """
        try:
            if session_id is None or not isinstance(session_id, str):
                return None
            # Prevent KeyError: 'UserSession'
            UserSession.load_from_file()

            user_session = UserSession.search({'session_id': session_id})
            # If the Session ID of the request is not linked to any User ID
            if not user_session:
                return None

            user_json = user_session[0].to_json()

            if self.session_duration <= 0:
                return user_json.get('user_id')
            # created_at = datetime.fromisoformat(user_json.get('created_at'))
            created_at = user_session[0].created_at
            expiration_time = created_at + timedelta(
                seconds=self.session_duration)
            if expiration_time < datetime.utcnow():
                return None
            return user_json.get('user_id')
        except Exception as e:
            print(f"An error occurred in user_id_for_session_id: {e}")
            return None

    def destroy_session(self, request=None):
        """ Destroy a UserSession instance based on a
        Session ID from a request cookie
        """
        try:
            if request is None:
                return False
            session_id = self.session_cookie(request)
            # Check if request doesn’t contain the Session ID cookie
            if not session_id:
                return False
            user_session = UserSession.search({'session_id': session_id})
            # If the Session ID of the request is not linked to any User ID
            if not user_session:
                return False
            user_session[0].remove()
            return True
        except Exception as e:
            print(f"An error occurred in destroy_session: {e}")
            return False
