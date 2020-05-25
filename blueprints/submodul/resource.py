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

from .model import Submoduls
from ..course.model import Courses
from ..week.model import Weeks
from ..modul.model import Moduls

bp_submodul = Blueprint("submodul", __name__)
api = Api(bp_submodul)


class SubmodulsResource(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self, id=None):
        qry = Submoduls.query.get(id)

        if qry is not None:
            submodul = marshal(qry, Submoduls.response_fields)
            modul_id = marshal(
                Moduls.query.filter_by(id=submodul["modul_id"]).all(),
                Moduls.response_fields,
            )
            submodul["modul_id"] = modul_id
            submodul["modul_id"][0]["week_id"] = marshal(
                Weeks.query.filter_by(id=submodul["modul_id"][0]["week_id"]).all(),
                Weeks.response_fields,
            )
            submodul["modul_id"][0]["week_id"][0]["course_id"] = marshal(
                Courses.query.filter_by(
                    id=submodul["modul_id"][0]["week_id"][0]["course_id"]
                ).all(),
                Courses.response_fields,
            )
            return submodul, 200

        return {"status": "NOT_FOUND"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("modul_id", location="json", required=True)
        parser.add_argument("name_submodul", location="json", required=True)
        args = parser.parse_args()

        qry_modul = Moduls.query.get(args["modul_id"])

        if qry_modul is not None:
            modul_id = marshal(qry_modul, Moduls.response_fields)

            submodul = Submoduls(args["modul_id"], args["name_submodul"])

            db.session.add(submodul)
            db.session.commit()

            submodul = marshal(submodul, Submoduls.response_fields)

            submodul["modul_id"] = modul_id
            submodul["modul_id"]["week_id"] = marshal(
                Weeks.query.filter_by(id=submodul["modul_id"]["week_id"]).all(),
                Weeks.response_fields,
            )
            submodul["modul_id"]["week_id"][0]["course_id"] = marshal(
                Courses.query.filter_by(
                    id=submodul["modul_id"]["week_id"][0]["course_id"]
                ).all(),
                Courses.response_fields,
            )

            return submodul, 200

        return {"status": "MODUL NOT FOUND"}, 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("modul_id", location="json", required=True)
        parser.add_argument("name_submodul", location="json", required=True)
        args = parser.parse_args()

        submodul = Submoduls.query.get(id)

        if submodul is not None:
            modul = Moduls.query.get(args["modul_id"])

            if modul is not None:
                submodul.modul_id = args["modul_id"]
                submodul.name_submodul = args["name_submodul"]
                db.session.commit()

                submodul = marshal(submodul, Submoduls.response_fields)

                modul_id = marshal(modul, Moduls.response_fields)
                submodul["modul_id"] = modul_id
                submodul["modul_id"]["week_id"] = marshal(
                    Weeks.query.filter_by(id=submodul["modul_id"]["week_id"]).all(),
                    Weeks.response_fields,
                )
                submodul["modul_id"]["week_id"][0]["course_id"] = marshal(
                    Courses.query.filter_by(
                        id=submodul["modul_id"]["week_id"][0]["course_id"]
                    ).all(),
                    Courses.response_fields,
                )

                return submodul, 200

            return {"status": "MODUL NOT FOUND"}, 404

        return {"status": "SUBMODUL NOT FOUND"}, 404

    def delete(self, id):
        submodul = Submoduls.query.get(id)

        if submodul is not None:
            db.session.delete(submodul)
            db.session.commit()
            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}


class SubmodulsAll(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self):
        submodul = Submoduls.query

        rows = []
        for row in submodul:
            row = marshal(row, Submoduls.response_fields)
            modul_id = marshal(
                Moduls.query.filter_by(id=row["modul_id"]).first(),
                Moduls.response_fields,
            )

            row["modul_id"] = modul_id

            row["modul_id"]["week_id"] = marshal(
                Weeks.query.filter_by(id=row["modul_id"]["week_id"]).all(),
                Weeks.response_fields,
            )

            row["modul_id"]["week_id"][0]["course_id"] = marshal(
                Courses.query.filter_by(
                    id=row["modul_id"]["week_id"][0]["course_id"]
                ).all(),
                Courses.response_fields,
            )

            rows.append(row)

        if rows == []:
            return {"status": "NOT_FOUND"}, 400

        return rows, 200


api.add_resource(SubmodulsAll, "")
api.add_resource(SubmodulsResource, "", "/<id>")
