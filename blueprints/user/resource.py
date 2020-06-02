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

        salt = uuid.uuid4().hex
        encoded = ("%s%s" % (args["pin"], salt)).encode("utf-8")
        hash_pass = hashlib.sha512(encoded).hexdigest()

        result = Users(
            args["username"],
            args["full_name"],
            hash_pass,
            args["place_birth"],
            args["date_birth"],
            args["address"],
            salt,
        )

        db.session.add(result)
        db.session.commit()

        jwt_username = marshal(result, Users.jwt_claims_fields)
        token = create_access_token(identity=args["username"], user_claims=jwt_username)

        result = marshal(result, Users.response_fields)
        result["token"] = token

        return result, 200


class UsersAll(Resource):
    def get(self):
        qry = Users.query

        rows = []
        for row in qry:
            rows.append(marshal(row, Users.response_fields))
        return rows, 200


api.add_resource(UsersAll, "")
api.add_resource(UsersResource, "", "/<id>")
