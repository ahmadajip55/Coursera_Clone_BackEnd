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

from .model import Courses

bp_course = Blueprint("course", __name__)
api = Api(bp_course)


class CoursesResource(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self, id=None):
        qry = Courses.query.get(id)

        if qry is not None:
            return marshal(qry, Courses.response_fields), 200

        return {"status": "NOT_FOUND"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name_course", location="json", required=True)
        parser.add_argument("description", location="json")
        args = parser.parse_args()

        result = Courses(args["name_course"], args["description"])

        db.session.add(result)
        db.session.commit()

        return marshal(result, Courses.response_fields), 200

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("name_course", location="json", required=True)
        parser.add_argument("description", location="json")
        args = parser.parse_args()

        course = Courses.query.get(id)

        if course is not None:
            course.name_course = args["name_course"]
            course.description = args["description"]
            db.session.commit()
            return marshal(course, Courses.response_fields), 200

        return {"status": "COURSE NOT FOUND"}, 404

    def delete(self, id):
        qry = Courses.query.get(id)

        if qry is not None:
            db.session.delete(qry)
            db.session.commit()
            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}, 404


class CoursesAll(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self):
        qry = Courses.query

        rows = []
        for row in qry:
            rows.append(marshal(row, Courses.response_fields))

        if rows == []:
            return {"status": "NOT_FOUND"}, 404

        return rows, 200


api.add_resource(CoursesAll, "")
api.add_resource(CoursesResource, "", "/<id>")
