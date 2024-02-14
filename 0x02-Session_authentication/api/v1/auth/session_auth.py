#!/usr/bin/env python3
""" Python Module """
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """ inherits from Auth """

    user_id_by_session_id = {}

    def session_cookie(self, request):
        """ Retrieve session cookie value from the request """
        return request.cookies.get('session_cookie_name')

    def create_session(self, user_id: str = None) -> str:
        """ creates a Session ID for a user_id
        """
        if user_id is None:
            return None
        if type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ user_id_for_session_id function """
        if session_id is None:
            return None
        if type(session_id) is None:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns a User instance """
        cookie_val = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_val)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ logout """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_id = self.user_id_for_session_id(session_id)

        if not user_id:
            return False

        try:
            del self.user_id_by_session_id[session_id]
        except Exception:
            pass

        return True
