from flask import request
from flask_restx import Resource, Namespace

from dao.model.genre import GenreSchema
from helpers.decorates import auth_required, admin_required
from implemented import genre_service

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        genre_service.create(GenreSchema().loads(request.data))
        return 'Genre created', 201

@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        g = genre_service.get_one(gid)
        sm_d = GenreSchema().dump(g)
        return sm_d, 200

    @admin_required
    def put(self, gid: int):
        genre_service.update(gid, GenreSchema().loads(request.data))
        return 'Genre changed', 204

    @admin_required
    def patch(self, gid: int):
        genre_service.partial_update(gid, GenreSchema().loads(request.data))
        return 'Genre changed', 204

    @admin_required
    def delete(self, gid: int):
        genre_service.delete(gid)
        return 'Genre deleted', 204