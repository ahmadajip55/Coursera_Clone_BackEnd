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

from .model import Questions
from ..course.model import Courses
from ..week.model import Weeks
from ..modul.model import Moduls
from ..quiz.model import Quizs

bp_question = Blueprint("question", __name__)
api = Api(bp_question)


class QuestionsResource(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self, id=None):
        qry = Questions.query.get(id)

        if qry is not None:
            question = marshal(qry, Questions.response_fields)
            quiz_id = marshal(
                Quizs.query.filter_by(id=question["quiz_id"]).all(),
                Quizs.response_fields,
            )
            question["quiz_id"] = quiz_id
            question["quiz_id"][0]["modul_id"] = marshal(
                Moduls.query.filter_by(id=question["quiz_id"][0]["modul_id"]).all(),
                Moduls.response_fields,
            )
            question["quiz_id"][0]["modul_id"][0]["week_id"] = marshal(
                Weeks.query.filter_by(
                    id=question["quiz_id"][0]["modul_id"][0]["week_id"]
                ).all(),
                Weeks.response_fields,
            )
            question["quiz_id"][0]["modul_id"][0]["week_id"][0]["course_id"] = marshal(
                Courses.query.filter_by(
                    id=question["quiz_id"][0]["modul_id"][0]["week_id"][0]["course_id"]
                ).all(),
                Courses.response_fields,
            )
            return question, 200

        return {"status": "NOT_FOUND"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("quiz_id", location="json", required=True)
        parser.add_argument("question", location="json")
        args = parser.parse_args()

        qry_quiz = Quizs.query.get(args["quiz_id"])

        if qry_quiz is not None:
            quiz_id = marshal(qry_quiz, Quizs.response_fields)

            question = Questions(args["quiz_id"], args["question"])

            db.session.add(question)
            db.session.commit()

            question = marshal(question, Questions.response_fields)

            question["quiz_id"] = quiz_id
            question["quiz_id"]["modul_id"] = marshal(
                Moduls.query.filter_by(id=question["quiz_id"]["modul_id"]).all(),
                Moduls.response_fields,
            )
            question["quiz_id"]["modul_id"][0]["week_id"] = marshal(
                Weeks.query.filter_by(
                    id=question["quiz_id"]["modul_id"][0]["week_id"]
                ).all(),
                Weeks.response_fields,
            )
            question["quiz_id"]["modul_id"][0]["week_id"][0]["course_id"] = marshal(
                Courses.query.filter_by(
                    id=question["quiz_id"]["modul_id"][0]["week_id"][0]["course_id"]
                ).all(),
                Courses.response_fields,
            )

            return question, 200

        return {"status": "QUIZ NOT FOUND"}, 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("quiz_id", location="json", required=True)
        parser.add_argument("question", location="json")
        args = parser.parse_args()

        question = Questions.query.get(id)

        if question is not None:
            quiz = Quizs.query.get(args["quiz_id"])

            if quiz is not None:
                question.quiz_id = args["quiz_id"]
                question.question = args["question"]
                db.session.commit()

                question = marshal(question, Questions.response_fields)

                quiz_id = marshal(quiz, Quizs.response_fields)
                question["quiz_id"] = quiz_id
                question["quiz_id"]["modul_id"] = marshal(
                    Moduls.query.filter_by(id=question["quiz_id"]["modul_id"]).all(),
                    Moduls.response_fields,
                )
                question["quiz_id"]["modul_id"][0]["week_id"] = marshal(
                    Weeks.query.filter_by(
                        id=question["quiz_id"]["modul_id"][0]["week_id"]
                    ).all(),
                    Weeks.response_fields,
                )
                question["quiz_id"]["modul_id"][0]["week_id"][0]["course_id"] = marshal(
                    Courses.query.filter_by(
                        id=question["quiz_id"]["modul_id"][0]["week_id"][0]["course_id"]
                    ).all(),
                    Courses.response_fields,
                )

                return question, 200

            return {"status": "QUIZ NOT FOUND"}, 404

        return {"status": "QUESTION NOT FOUND"}, 404

    def delete(self, id):
        question = Questions.query.get(id)

        if question is not None:
            db.session.delete(question)
            db.session.commit()
            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}


class QuestionsAll(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self):
        question = Questions.query

        rows = []
        for row in question:
            row = marshal(row, Questions.response_fields)
            quiz_id = marshal(
                Quizs.query.filter_by(id=row["quiz_id"]).first(), Quizs.response_fields,
            )

            row["quiz_id"] = quiz_id

            row["quiz_id"]["modul_id"] = marshal(
                Moduls.query.filter_by(id=row["quiz_id"]["modul_id"]).all(),
                Moduls.response_fields,
            )

            row["quiz_id"]["modul_id"][0]["week_id"] = marshal(
                Weeks.query.filter_by(
                    id=row["quiz_id"]["modul_id"][0]["week_id"]
                ).all(),
                Weeks.response_fields,
            )
            row["quiz_id"]["modul_id"][0]["week_id"][0]["course_id"] = marshal(
                Courses.query.filter_by(
                    id=row["quiz_id"]["modul_id"][0]["week_id"][0]["course_id"]
                ).all(),
                Courses.response_fields,
            )

            rows.append(row)

        if rows == []:
            return {"status": "NOT_FOUND"}, 400

        return rows, 200


api.add_resource(QuestionsAll, "")
api.add_resource(QuestionsResource, "", "/<id>")
