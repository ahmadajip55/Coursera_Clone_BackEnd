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

from .model import Moduls
from ..course.model import Courses
from ..week.model import Weeks

bp_modul = Blueprint("modul", __name__)
api = Api(bp_modul)


class ModulsResource(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self, id=None):
        qry = Moduls.query.get(id)

        if qry is not None:
            modul = marshal(qry, Moduls.response_fields)
            week_id = marshal(
                Weeks.query.filter_by(id=modul["week_id"]).all(), Weeks.response_fields
            )
            modul["week_id"] = week_id
            modul["week_id"][0]["course_id"] = marshal(
                Courses.query.filter_by(id=modul["week_id"][0]["course_id"]).all(),
                Courses.response_fields,
            )
            return modul, 200

        return {"status": "NOT_FOUND"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("week_id", location="json", required=True)
        parser.add_argument("name_modul", location="json", required=True)
        parser.add_argument("description", location="json", required=True)
        args = parser.parse_args()

        qry_week = Weeks.query.get(args["week_id"])

        if qry_week is not None:
            modul = Moduls(args["week_id"], args["name_modul"], args["description"])

            db.session.add(modul)
            db.session.commit()

            modul = marshal(modul, Moduls.response_fields)
            week_id = marshal(qry_week, Weeks.response_fields)
            modul["week_id"] = week_id

            modul["week_id"]["course_id"] = marshal(
                Courses.query.filter_by(id=modul["week_id"]["course_id"]).all(),
                Courses.response_fields,
            )

            return modul, 200

        return {"status": "WEEK NOT FOUND"}, 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("week_id", location="json", required=True)
        parser.add_argument("name_modul", location="json", required=True)
        parser.add_argument("description", location="json", required=True)
        args = parser.parse_args()

        qry_week = Weeks.query.get(args["week_id"])

        if qry_week is not None:
            modul = Moduls.query.get(id)

            if modul is not None:
                modul.week_id = args["week_id"]
                modul.name_modul = args["name_modul"]
                modul.description = args["description"]
                db.session.commit()

                modul = marshal(modul, Moduls.response_fields)

                week_id = marshal(qry_week, Weeks.response_fields)
                modul["week_id"] = week_id

                modul["week_id"]["course_id"] = marshal(
                    Courses.query.filter_by(id=modul["week_id"]["course_id"]).all(),
                    Courses.response_fields,
                )

                return modul, 200

            return {"status": "MODUL NOT FOUND"}, 200

        return {"status": "WEEK NOT FOUND"}, 404

    def delete(self, id):
        modul = Moduls.query.get(id)

        if modul is not None:
            db.session.delete(modul)
            db.session.commit()
            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}


class ModulsAll(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self):
        modul = Moduls.query

        rows = []
        for row in modul:
            row = marshal(row, Moduls.response_fields)
            week_id = marshal(
                Weeks.query.filter_by(id=row["week_id"]).first(), Weeks.response_fields
            )

            row["week_id"] = week_id

            row["week_id"]["course_id"] = marshal(
                Courses.query.filter_by(id=row["week_id"]["course_id"]).all(),
                Courses.response_fields,
            )

            rows.append(row)

        if rows == []:
            return {"status": "NOT_FOUND"}, 400

        return rows, 200


api.add_resource(ModulsAll, "")
api.add_resource(ModulsResource, "", "/<id>")
