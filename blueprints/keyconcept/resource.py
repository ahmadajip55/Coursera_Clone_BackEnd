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

from .model import KeyConcepts
from ..course.model import Courses
from ..week.model import Weeks
from ..modul.model import Moduls

bp_keyconcept = Blueprint("keyconcept", __name__)
api = Api(bp_keyconcept)


class KeyConceptsResource(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self, id=None):
        qry = KeyConcepts.query.get(id)

        if qry is not None:
            keyconcept = marshal(KeyConcepts.query.get(id), KeyConcepts.response_fields)
            modul_id = marshal(
                Moduls.query.filter_by(id=keyconcept["modul_id"]).all(),
                Moduls.response_fields,
            )
            keyconcept["modul_id"] = modul_id
            keyconcept["modul_id"][0]["week_id"] = marshal(
                Weeks.query.filter_by(id=keyconcept["modul_id"][0]["week_id"]).all(),
                Weeks.response_fields,
            )
            keyconcept["modul_id"][0]["week_id"][0]["course_id"] = marshal(
                Courses.query.filter_by(
                    id=keyconcept["modul_id"][0]["week_id"][0]["course_id"]
                ).all(),
                Courses.response_fields,
            )
            return keyconcept, 200

        return {"status": "NOT_FOUND"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("modul_id", location="json", required=True)
        parser.add_argument("concept", location="json", required=True)
        args = parser.parse_args()

        qry_modul = Moduls.query.get(args["modul_id"])

        if qry_modul is not None:
            keyconcept = KeyConcepts(args["modul_id"], args["concept"])

            db.session.add(keyconcept)
            db.session.commit()

            keyconcept = marshal(keyconcept, KeyConcepts.response_fields)

            modul_id = marshal(qry_modul, Moduls.response_fields)
            keyconcept["modul_id"] = modul_id
            keyconcept["modul_id"]["week_id"] = marshal(
                Weeks.query.filter_by(id=keyconcept["modul_id"]["week_id"]).all(),
                Weeks.response_fields,
            )
            keyconcept["modul_id"]["week_id"][0]["course_id"] = marshal(
                Courses.query.filter_by(
                    id=keyconcept["modul_id"]["week_id"][0]["course_id"]
                ).all(),
                Courses.response_fields,
            )

            return keyconcept, 200

        return {"status": "MODUL NOT FOUND"}, 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("modul_id", location="json", required=True)
        parser.add_argument("concept", location="json", required=True)
        args = parser.parse_args()

        keyconcept = KeyConcepts.query.get(id)

        if keyconcept is not None:
            modul = Moduls.query.get(args["modul_id"])

            if modul is not None:
                keyconcept.modul_id = args["modul_id"]
                keyconcept.concept = args["concept"]
                db.session.commit()

                keyconcept = marshal(keyconcept, KeyConcepts.response_fields)

                modul_id = marshal(modul, Moduls.response_fields)
                keyconcept["modul_id"] = modul_id
                keyconcept["modul_id"]["week_id"] = marshal(
                    Weeks.query.filter_by(id=keyconcept["modul_id"]["week_id"]).all(),
                    Weeks.response_fields,
                )
                keyconcept["modul_id"]["week_id"][0]["course_id"] = marshal(
                    Courses.query.filter_by(
                        id=keyconcept["modul_id"]["week_id"][0]["course_id"]
                    ).all(),
                    Courses.response_fields,
                )

                return keyconcept, 200

            return {"status": "MODUL NOT FOUND"}, 404

        return {"status": "KEYCONCEPT NOT FOUND"}, 404

    def delete(self, id):
        keyconcept = KeyConcepts.query.get(id)

        if keyconcept is not None:
            db.session.delete(keyconcept)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}, 404


class KeyConceptsAll(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self):
        keyconcept = KeyConcepts.query

        rows = []
        for row in keyconcept:
            row = marshal(row, KeyConcepts.response_fields)
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
            return {"status": "NOT_FOUND"}, 404

        return rows, 200


api.add_resource(KeyConceptsAll, "")
api.add_resource(KeyConceptsResource, "", "/<id>")
