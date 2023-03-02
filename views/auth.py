from flask import request, jsonify
from flask_restx import Resource, Namespace

from dao.model.user import UserSchema
from implemented import user_service, auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
        auth_data = request.json
        username = auth_data.get("username")
        password = auth_data.get("password")

        if None in [username, password]:
            return "", 400

        tokens = auth_service.generate_tokens(username, password)
        return tokens

