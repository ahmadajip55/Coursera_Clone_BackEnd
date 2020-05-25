import json
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs
from blueprints import db, app
from sqlalchemy import desc
import hashlib, uuid
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
    get_jwt_claims,
)

from .model import Users

bp_user = Blueprint("user", __name__)
api = Api(bp_user)


class UsersResource(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self, id=None):
        qry = Users.query.get(id)
        if qry is not None:
            return marshal(qry, Users.response_fields), 200

        return {"status": "NOT_FOUND"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", location="json", required=True)
        parser.add_argument("full_name", location="json")
        parser.add_argument("pin", location="json", required=True)
        parser.add_argument("place_birth", location="json")
        parser.add_argument("date_birth", location="json")
        parser.add_argument("address", location="json")
        args = parser.parse_args()

        result = Users(
            args["username"],
            args["full_name"],
            args["pin"],
            args["place_birth"],
            args["date_birth"],
            args["address"],
        )

        db.session.add(result)
        db.session.commit()

        return marshal(result, Users.response_fields), 200


class UsersAll(Resource):
    def get(self):
        qry = Users.query

        rows = []
        for row in qry:
            rows.append(marshal(row, Users.response_fields))
        return rows, 200


api.add_resource(UsersAll, "")
api.add_resource(UsersResource, "", "/<id>")
