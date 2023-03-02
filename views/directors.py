from flask import request
from flask_restx import Resource, Namespace

from dao.model.director import DirectorSchema
from helpers.decorates import auth_required, admin_required
from implemented import director_service

director_ns = Namespace('directors')


@director_ns.route('/')
class DirectorsView(Resource):
    @auth_required
    def get(self):
        rs = director_service.get_all()
        res = DirectorSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        director_service.create(DirectorSchema().loads(request.data))
        return 'Director created', 201


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    @auth_required
    def get(self, did):
        d = director_service.get_one(did)
        sm_d = DirectorSchema().dump(d)
        return sm_d, 200

    @admin_required
    def put(self, did: int):
        director_service.update(did, DirectorSchema().loads(request.data))
        return 'Director changed', 204

    @admin_required
    def patch(self, did: int):
        director_service.partial_update(did, DirectorSchema().loads(request.data))
        return 'Director changed', 204

    @admin_required
    def delete(self, did: int):
        director_service.delete(did)
        return 'Director deleted', 204