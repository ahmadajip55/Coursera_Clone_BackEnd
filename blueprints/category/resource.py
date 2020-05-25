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

from .model import Categories

bp_category = Blueprint("category", __name__)
api = Api(bp_category)


class CategoriesResource(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self, id=None):
        qry = Categories.query.get(id)
        if qry is not None:
            return marshal(qry, Categories.response_fields), 200
        return {"status": "NOT_FOUND"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name_category", location="json", required=True)
        args = parser.parse_args()

        result = Categories(args["name_category"])

        db.session.add(result)
        db.session.commit()

        return marshal(result, Categories.response_fields), 200

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("name_category", location="json", required=True)
        args = parser.parse_args()

        category = Categories.query.get(id)

        if category is not None:
            category.name_category = args["name_category"]
            db.session.commit()
            return marshal(category, Categories.response_fields), 200

        return {"status": "CATEGORY NOT FOUND"}, 404

    def delete(self, id):
        qry = Categories.query.get(id)

        if qry is not None:
            db.session.delete(qry)
            db.session.commit()
            return {"status": "DELETED SUCCESS"}, 200
        return {"status": "NOT_FOUND"}, 404


class CategoriesAll(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self):
        qry = Categories.query

        rows = []
        for row in qry:
            rows.append(marshal(row, Categories.response_fields))

        if rows == []:
            return {"status": "NOT_FOUND"}, 404
        return rows, 200


api.add_resource(CategoriesAll, "")
api.add_resource(CategoriesResource, "", "/<id>")
