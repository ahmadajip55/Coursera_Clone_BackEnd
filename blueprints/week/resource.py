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

from .model import Weeks
from ..course.model import Courses

bp_week = Blueprint("week", __name__)
api = Api(bp_week)


class WeeksResource(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self, id=None):
        qry = Weeks.query.get(id)
        week = marshal(qry, Weeks.response_fields)
        course_id = marshal(
            Courses.query.filter_by(id=week["course_id"]).all(), Courses.response_fields
        )
        week["course_id"] = course_id

        if qry is not None:
            return week, 200

        return {"status": "NOT_FOUND"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("course_id", location="json", required=True)
        parser.add_argument("name_week", location="json", required=True)
        args = parser.parse_args()

        qry_course = Courses.query.get(args["course_id"])

        if qry_course is not None:
            week = Weeks(args["course_id"], args["name_week"])

            db.session.add(week)
            db.session.commit()

            week = marshal(week, Weeks.response_fields)
            course_id = marshal(qry_course, Courses.response_fields)
            week["course_id"] = course_id

            return week, 200

        return {"status": "COURSE NOT FOUND"}, 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("course_id", location="json", required=True)
        parser.add_argument("name_week", location="json", required=True)
        args = parser.parse_args()

        qry_course = Courses.query.get(args["course_id"])

        if qry_course is not None:
            week = Weeks.query.get(id)

            if week is not None:
                week.course_id = args["course_id"]
                week.name_week = args["name_week"]
                db.session.commit()

                week = marshal(week, Weeks.response_fields)
                course_id = marshal(qry_course, Courses.response_fields)
                week["course_id"] = course_id

                return week, 200

            return {"status": "WEEK NOT FOUND"}, 404

        return {"status": "COURSE NOT FOUND"}, 404

    def delete(self, id):
        week = Weeks.query.get(id)

        if week is not None:
            db.session.delete(week)
            db.session.commit()
            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}, 404


class WeeksAll(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    # endpoint menampilkan semua week dan atau endpoint menampilkan semua week dalam 1 course
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("course_id", type=int, location="args")
        args = parser.parse_args()

        week = Weeks.query

        id_course = args["course_id"]
        if id_course is None:
            rows = []
            for row in week:
                row = marshal(row, Weeks.response_fields)
                course_id = marshal(
                    Courses.query.filter_by(id=row["course_id"]).first(),
                    Courses.response_fields,
                )
                row["course_id"] = course_id
                rows.append(row)
        else:
            rows = []
            for row in week:
                if row.course_id == id_course:
                    row = marshal(row, Weeks.response_fields)
                    course_id = marshal(
                        Courses.query.filter_by(id=row["course_id"]).first(),
                        Courses.response_fields,
                    )
                    row["course_id"] = course_id
                    rows.append(row)

        if rows == []:
            return {"status": "NOT_FOUND"}, 400

        return rows, 200


api.add_resource(WeeksAll, "")
api.add_resource(WeeksResource, "", "/<id>")
