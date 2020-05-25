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

from .model import Choices
from ..course.model import Courses
from ..week.model import Weeks
from ..modul.model import Moduls
from ..quiz.model import Quizs
from ..question.model import Questions

bp_choice = Blueprint("choice", __name__)
api = Api(bp_choice)


class ChoicesResource(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self, id=None):
        qry = Choices.query.get(id)

        if qry is not None:
            choice = marshal(qry, Choices.response_fields)
            question_id = marshal(
                Questions.query.filter_by(id=choice["question_id"]).all(),
                Questions.response_fields,
            )
            choice["question_id"] = question_id
            choice["question_id"][0]["quiz_id"] = marshal(
                Quizs.query.filter_by(id=choice["question_id"][0]["quiz_id"]).all(),
                Quizs.response_fields,
            )
            choice["question_id"][0]["quiz_id"][0]["modul_id"] = marshal(
                Moduls.query.filter_by(
                    id=choice["question_id"][0]["quiz_id"][0]["modul_id"]
                ).all(),
                Moduls.response_fields,
            )
            choice["question_id"][0]["quiz_id"][0]["modul_id"][0]["week_id"] = marshal(
                Weeks.query.filter_by(
                    id=choice["question_id"][0]["quiz_id"][0]["modul_id"][0]["week_id"]
                ).all(),
                Weeks.response_fields,
            )
            return choice, 200

        return {"status": "NOT_FOUND"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("question_id", location="json", required=True)
        parser.add_argument("choice", location="json")
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()

        qry_question = Questions.query.get(args["question_id"])

        if qry_question is not None:
            question_id = marshal(qry_question, Questions.response_fields)

            choice = Choices(args["question_id"], args["choice"], args["status"])

            db.session.add(choice)
            db.session.commit()

            choice = marshal(choice, Choices.response_fields)

            choice["question_id"] = question_id
            choice["question_id"]["quiz_id"] = marshal(
                Quizs.query.filter_by(id=choice["question_id"]["quiz_id"]).all(),
                Quizs.response_fields,
            )
            choice["question_id"]["quiz_id"][0]["modul_id"] = marshal(
                Moduls.query.filter_by(
                    id=choice["question_id"]["quiz_id"][0]["modul_id"]
                ).all(),
                Moduls.response_fields,
            )
            choice["question_id"]["quiz_id"][0]["modul_id"][0]["week_id"] = marshal(
                Weeks.query.filter_by(
                    id=choice["question_id"]["quiz_id"][0]["modul_id"][0]["week_id"]
                ).all(),
                Weeks.response_fields,
            )

            return choice, 200

        return {"status": "QUESTION NOT FOUND"}, 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("question_id", location="json", required=True)
        parser.add_argument("choice", location="json")
        parser.add_argument("status", location="json", type=bool)
        args = parser.parse_args()

        choice = Choices.query.get(id)

        if choice is not None:
            question = Questions.query.get(args["question_id"])

            if question is not None:
                choice.question_id = args["question_id"]
                choice.choice = args["choice"]
                choice.status = args["status"]
                db.session.commit()

                choice = marshal(choice, Choices.response_fields)

                question_id = marshal(question, Questions.response_fields)
                choice["question_id"] = question_id
                choice["question_id"]["quiz_id"] = marshal(
                    Quizs.query.filter_by(id=choice["question_id"]["quiz_id"]).all(),
                    Quizs.response_fields,
                )
                choice["question_id"]["quiz_id"][0]["modul_id"] = marshal(
                    Moduls.query.filter_by(
                        id=choice["question_id"]["quiz_id"][0]["modul_id"]
                    ).all(),
                    Moduls.response_fields,
                )
                choice["question_id"]["quiz_id"][0]["modul_id"][0]["week_id"] = marshal(
                    Weeks.query.filter_by(
                        id=choice["question_id"]["quiz_id"][0]["modul_id"][0]["week_id"]
                    ).all(),
                    Weeks.response_fields,
                )

                return choice, 200

            return {"status": "QUESTION NOT FOUND"}, 404

        return {"status": "CHOICE NOT FOUND"}, 404

    def delete(self, id):
        choice = Choices.query.get(id)

        if choice is not None:
            db.session.delete(choice)
            db.session.commit()

            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}


class ChoicesAll(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self):
        choice = Choices.query

        rows = []
        for row in choice:
            row = marshal(row, Choices.response_fields)
            question_id = marshal(
                Questions.query.filter_by(id=row["question_id"]).first(),
                Questions.response_fields,
            )

            row["question_id"] = question_id

            row["question_id"]["quiz_id"] = marshal(
                Quizs.query.filter_by(id=row["question_id"]["quiz_id"]).all(),
                Quizs.response_fields,
            )

            row["question_id"]["quiz_id"][0]["modul_id"] = marshal(
                Moduls.query.filter_by(
                    id=row["question_id"]["quiz_id"][0]["modul_id"]
                ).all(),
                Moduls.response_fields,
            )

            row["question_id"]["quiz_id"][0]["modul_id"][0]["week_id"] = marshal(
                Weeks.query.filter_by(
                    id=row["question_id"]["quiz_id"][0]["modul_id"][0]["week_id"]
                ).all(),
                Weeks.response_fields,
            )

            rows.append(row)

        if rows == []:
            return {"status": "NOT_FOUND"}, 400

        return rows, 200


api.add_resource(ChoicesAll, "")
api.add_resource(ChoicesResource, "", "/<id>")
