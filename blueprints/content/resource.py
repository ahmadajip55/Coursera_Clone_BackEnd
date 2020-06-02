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

from .model import Contents
from ..course.model import Courses
from ..week.model import Weeks
from ..modul.model import Moduls
from ..submodul.model import Submoduls
from ..category.model import Categories
from ..quiz.model import Quizs

bp_content = Blueprint("content", __name__)
api = Api(bp_content)


class ContentsResource(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self, id=None):
        qry = Contents.query.get(id)

        if qry is not None:
            content = marshal(qry, Contents.response_fields)
            submodul_id = marshal(
                Submoduls.query.filter_by(id=content["submodul_id"]).all(),
                Submoduls.response_fields,
            )
            category_id = marshal(
                Categories.query.get(content["category_id"]), Categories.response_fields
            )

            content["submodul_id"] = submodul_id
            content["submodul_id"][0]["modul_id"] = marshal(
                Moduls.query.filter_by(id=content["submodul_id"][0]["modul_id"]).all(),
                Moduls.response_fields,
            )
            content["submodul_id"][0]["modul_id"][0]["week_id"] = marshal(
                Weeks.query.filter_by(
                    id=content["submodul_id"][0]["modul_id"][0]["week_id"]
                ).all(),
                Weeks.response_fields,
            )
            content["submodul_id"][0]["modul_id"][0]["week_id"][0][
                "course_id"
            ] = marshal(
                Courses.query.filter_by(
                    id=content["submodul_id"][0]["modul_id"][0]["week_id"][0][
                        "course_id"
                    ]
                ).all(),
                Courses.response_fields,
            )
            content["category_id"] = category_id

            return content, 200

        return {"status": "NOT_FOUND"}, 404

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("submodul_id", location="json", required=True)
        parser.add_argument("category_id", location="json", required=True)
        parser.add_argument("name_content", location="json", required=True)
        parser.add_argument("content", location="json", required=True)
        parser.add_argument("description", location="json", required=True)
        parser.add_argument("duration", location="json", required=True)
        args = parser.parse_args()

        qry_submodul = Submoduls.query.get(args["submodul_id"])
        qry_category = Categories.query.get(args["category_id"])

        if qry_submodul is not None and qry_category is not None:
            submodul_id = marshal(qry_submodul, Submoduls.response_fields)
            category_id = marshal(qry_category, Categories.response_fields)

            content = Contents(
                args["submodul_id"],
                args["category_id"],
                args["name_content"],
                args["content"],
                args["description"],
                args["duration"],
            )

            db.session.add(content)
            db.session.commit()

            content = marshal(content, Contents.response_fields)

            content["submodul_id"] = submodul_id
            content["submodul_id"]["modul_id"] = marshal(
                Moduls.query.filter_by(id=content["submodul_id"]["modul_id"]).all(),
                Moduls.response_fields,
            )
            content["submodul_id"]["modul_id"][0]["week_id"] = marshal(
                Weeks.query.filter_by(
                    id=content["submodul_id"]["modul_id"][0]["week_id"]
                ).all(),
                Weeks.response_fields,
            )

            content["category_id"] = category_id

            return content, 200

        return {"status": "NOT FOUND"}, 404

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("submodul_id", location="json", required=True)
        parser.add_argument("category_id", location="json", required=True)
        parser.add_argument("name_content", location="json", required=True)
        parser.add_argument("content", location="json", required=True)
        parser.add_argument("description", location="json", required=True)
        parser.add_argument("duration", location="json", required=True)
        args = parser.parse_args()

        content = Contents.query.get(id)

        if content is not None:
            submodul = Submoduls.query.get(args["submodul_id"])

            if submodul is not None:
                category = Categories.query.get(args["category_id"])

                if category is not None:
                    content.submodul_id = args["submodul_id"]
                    content.category_id = args["category_id"]
                    content.name_content = args["name_content"]
                    content.content = args["content"]
                    content.description = args["description"]
                    content.duration = args["duration"]
                    db.session.commit()

                    submodul_id = marshal(submodul, Submoduls.response_fields)
                    category_id = marshal(category, Categories.response_fields)

                    content = marshal(content, Contents.response_fields)

                    content["submodul_id"] = submodul_id
                    content["submodul_id"]["modul_id"] = marshal(
                        Moduls.query.filter_by(
                            id=content["submodul_id"]["modul_id"]
                        ).all(),
                        Moduls.response_fields,
                    )
                    content["submodul_id"]["modul_id"][0]["week_id"] = marshal(
                        Weeks.query.filter_by(
                            id=content["submodul_id"]["modul_id"][0]["week_id"]
                        ).all(),
                        Weeks.response_fields,
                    )

                    content["category_id"] = category_id

                    return content, 200

                return {"status": "CATEGORY NOT FOUND"}, 404

            return {"status": "SUBMODUL NOT FOUND"}, 404

        return {"status": "CONTENT NOT FOUND"}, 404

    def delete(self, id):
        content = Contents.query.get(id)

        if content is not None:
            db.session.delete(content)
            db.session.commit()
            return {"status": "DELETED SUCCESS"}, 200

        return {"status": "NOT_FOUND"}


class ContentsAll(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self):
        content = Contents.query

        rows = []
        for row in content:
            row = marshal(row, Contents.response_fields)
            submodul_id = marshal(
                Submoduls.query.filter_by(id=row["submodul_id"]).first(),
                Submoduls.response_fields,
            )
            category_id = marshal(
                Categories.query.get(row["category_id"]), Categories.response_fields
            )

            row["submodul_id"] = submodul_id

            row["submodul_id"]["modul_id"] = marshal(
                Moduls.query.filter_by(id=row["submodul_id"]["modul_id"]).all(),
                Moduls.response_fields,
            )

            row["submodul_id"]["modul_id"][0]["week_id"] = marshal(
                Weeks.query.filter_by(
                    id=row["submodul_id"]["modul_id"][0]["week_id"]
                ).all(),
                Weeks.response_fields,
            )

            row["category_id"] = category_id

            rows.append(row)

        if rows == []:
            return {"status": "NOT_FOUND"}, 400

        return rows, 200


class ContentsCategory(Resource):
    def option(self, id=None):
        return {"status": "ok"}, 200

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("course_id", location="args", required=True)
        args = parser.parse_args()

        qry_weeks = Weeks.query.filter_by(course_id=args["course_id"]).all()
        weeks = []
        obj_weeks = marshal(qry_weeks, Weeks.response_fields)

        for week in obj_weeks:
            qry_moduls = Moduls.query.filter_by(week_id=week["id"]).all()
            obj_moduls = marshal(qry_moduls, Moduls.response_fields)
            week["modul"] = obj_moduls
            index_modul = 0
            total_duration = 0

            for modul in obj_moduls:
                qry_categories = Categories.query.all()
                obj_categories = marshal(qry_categories, Categories.response_fields)
                initial_categories = {}
                duration = 0
                for category in obj_categories:
                    initial_categories[category["name_category"]] = 0

                qry_quiz = Quizs.query.filter_by(modul_id=modul["id"]).all()
                obj_quiz = marshal(qry_quiz, Quizs.response_fields)

                qry_submoduls = Submoduls.query.filter_by(modul_id=modul["id"]).all()
                obj_submoduls = marshal(qry_submoduls, Submoduls.response_fields)
                week["modul"][index_modul]["submodul"] = obj_submoduls

                index_submodul = 0
                for submodul in obj_submoduls:
                    qry_contents = Contents.query.filter_by(
                        submodul_id=submodul["id"]
                    ).all()
                    obj_contents = marshal(qry_contents, Contents.response_fields)
                    week["modul"][index_modul]["submodul"][index_submodul][
                        "content"
                    ] = obj_contents

                    index_content = 0
                    for content in obj_contents:
                        for category in obj_categories:
                            if content["category_id"] == category["id"]:
                                initial_categories[
                                    category["name_category"]
                                ] += content["duration"]
                                duration += content["duration"]
                        index_content += 1

                    index_submodul += 1

                    week["modul"][index_modul][
                        "content_duration_minute"
                    ] = initial_categories
                    week["modul"][index_modul]["quiz_duration_minute"] = obj_quiz[0][
                        "duration_minute"
                    ]
                    week["modul"][index_modul]["total_duration_minute"] = (
                        duration + obj_quiz[0]["duration_minute"]
                    )

                total_duration += week["modul"][index_modul]["total_duration_minute"]

                index_modul += 1

            week["total_duration_minute"] = total_duration

            weeks.append(week)

        return weeks, 200


api.add_resource(ContentsAll, "")
api.add_resource(ContentsCategory, "", "/category")
api.add_resource(ContentsResource, "", "/<id>")
