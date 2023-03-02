import calendar
import datetime

import jwt
from flask import abort

from helpers.constants import JWT_SECRET, JWT_ALGORITHM
from service.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password):
        user_ = self.user_service.get_by_username(username)
        if user_ is None:
            abort(404)

        if not self.user_service.compare_password(user_.password, password):
            abort(400)

        data = {'username': user_.username, 'role': user_.role}

        # access token
        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, JWT_ALGORITHM)
        # refresh token
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, JWT_ALGORITHM)

        return {"access_token": access_token, "refresh_token": refresh_token}
