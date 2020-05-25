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

from blueprints.user.model import Users

bp_auth = Blueprint("auth", __name__)
api = Api(bp_auth)


class AuthResource(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", location="json", required=True)
        parser.add_argument("pin", location="json", required=True)
        args = parser.parse_args()

        qry_username = Users.query.filter_by(username=args["username"]).first()

        if qry_username:
            username_salt = qry_username.salt

            encoded = ("%s%s" % (args["pin"], username_salt)).encode("utf-8")
            hash_pass = hashlib.sha512(encoded).hexdigest()

            if hash_pass == qry_username.pin:
                obj_username = marshal(qry_username, Users.response_fields)
                jwt_username = marshal(qry_username, Users.jwt_claims_fields)
                token = create_access_token(
                    identity=args["username"], user_claims=jwt_username
                )
                obj_username["token"] = token
                return obj_username, 200

            else:
                return {"status": "pin wrong"}, 404

        else:
            return {"status": "username not registered"}, 404


api.add_resource(AuthResource, "")
