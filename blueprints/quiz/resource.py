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

from .model import Quizs
from ..course.model import Courses
from ..week.model import Weeks
from ..modul.model import Moduls

bp_quiz = Blueprint("quiz", __name__)
api = Api(bp_quiz)


class QuizsResource(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self, id=None):
        qry = Quizs.query.get(id)

        if qry is not None:
            quiz = marshal(qry, Quizs.response_fields)
            modul_id = marshal(
                Moduls.query.filter_by(id=quiz["modul_id"]).all(),
                Moduls.response_fields,
            )
            quiz["modul_id"] = modul_id
            quiz["modul_id"][0]["week_id"] = marshal(
                Weeks.query.filter_by(id=quiz["modul_id"][0]["week_id"]).all(),
                Weeks.response_fields,
            )
            quiz["modul_id"][0]["week_id"][0]["course_id"] = marshal(
                Courses.query.filter_by(
                    id=quiz["modul_id"][0]["week_id"][0]["course_id"]
                ).all(),
                Courses.response_fields,
            )
            return quiz, 200

        return {"status": "NOT_FOUND"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("modul_id", location="json", required=True)
        parser.add_argument("duration_minute", location="json")
        parser.add_argument("grade", location="json")
        args = parser.parse_args()

        qry_modul = Moduls.query.get(args["modul_id"])

        if qry_modul is not None:
            modul_id = marshal(qry_modul, Moduls.response_fields)

            quiz = Quizs(
                args["modul_id"],
                modul_id["name_modul"],
                args["duration_minute"],
                args["grade"],
            )

            db.session.add(quiz)
            db.session.commit()

            quiz = marshal(quiz, Quizs.response_fields)

            quiz["modul_id"] = modul_id
            quiz["modul_id"]["week_id"] = marshal(
                Weeks.query.filter_by(id=quiz["modul_id"]["week_id"]).all(),
                Weeks.response_fields,
            )
            quiz["modul_id"]["week_id"][0]["course_id"] = marshal(
                Courses.query.filter_by(
                    id=quiz["modul_id"]["week_id"][0]["course_id"]
                ).all(),
                Courses.response_fields,
            )

            return quiz, 200

        return {"status": "MODUL NOT FOUND"}, 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("modul_id", location="json", required=True)
        parser.add_argument("duration_minute", location="json")
        parser.add_argument("grade", location="json")
        args = parser.parse_args()

        quiz = Quizs.query.get(id)

        if quiz is not None:
            modul = Moduls.query.get(args["modul_id"])

            if modul is not None:
                quiz.modul_id = args["modul_id"]
                quiz.duration_minute = args["duration_minute"]
                quiz.grade = args["grade"]
                db.session.commit()

                quiz = marshal(quiz, Quizs.response_fields)

                modul_id = marshal(modul, Moduls.response_fields)
                quiz["modul_id"] = modul_id
                quiz["modul_id"]["week_id"] = marshal(
                    Weeks.query.filter_by(id=quiz["modul_id"]["week_id"]).all(),
                    Weeks.response_fields,
                )
                quiz["modul_id"]["week_id"][0]["course_id"] = marshal(
                    Courses.query.filter_by(
                        id=quiz["modul_id"]["week_id"][0]["course_id"]
                    ).all(),
                    Courses.response_fields,
                )

                return quiz, 200

            return {"status": "MODUL NOT FOUND"}, 404

        return {"status": "QUIZ NOT FOUND"}, 404

    def delete(self, id):
        quiz = Quizs.query.get(id)

        if quiz is not None:
            db.session.delete(quiz)
            db.session.commit()
            return {"status": "DELETED SUCCESS"}, 200
        return {"status": "NOT_FOUND"}


class QuizsAll(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self):
        quiz = Quizs.query

        rows = []
        for row in quiz:
            row = marshal(row, Quizs.response_fields)
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


api.add_resource(QuizsAll, "")
api.add_resource(QuizsResource, "", "/<id>")
