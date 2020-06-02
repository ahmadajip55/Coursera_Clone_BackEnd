import json, config, os
from flask import Flask, request
from functools import wraps

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from flask_script import Manager
from flask_cors import CORS

app = Flask(__name__)
CORS(
    app,
    origins="*",
    allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"],
    supports_credentials=True,
    intercept_exceptions=False,
)

if os.environ.get("FLASK_ENV", "Production") == "Production":
    app.config.from_object(config.ProductionConfig)
elif os.environ.get("FLASK_ENV", "Production") == "Testing":
    app.config.from_object(config.TestingConfig)
else:
    app.config.from_object(config.DevelopmentConfig)

jwt = JWTManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command("db", MigrateCommand)


@app.before_request
def before_request():
    if request.method != "OPTIONS":  # <-- required
        pass
    else:
        # ternyata cors pake method options di awal buat ngecek CORS dan harus di return kosong 200, jadi di akalin gini deh. :D
        return (
            {},
            200,
            {"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "*"},
        )


@app.after_request
def after_request(response):
    try:
        requestData = request.get_json()
    except Exception as e:
        requestData = request.args.to_dict()
    if response.status_code == 200:
        app.logger.warning(
            "REQUEST_LOG\t%s",
            json.dumps(
                {
                    "method": request.method,
                    "code": response.status,
                    "uri": request.full_path,
                    "request": requestData,
                    "response": json.loads(response.data.decode("utf-8")),
                }
            ),
        )
    else:
        app.logger.error(
            "REQUEST_LOG\t%s",
            json.dumps(
                {
                    "method": request.method,
                    "code": response.status,
                    "uri": request.full_path,
                    "request": requestData,
                    "response": json.loads(response.data.decode("utf-8")),
                }
            ),
        )
    return response


from blueprints.user.resource import bp_user
from blueprints.course.resource import bp_course
from blueprints.week.resource import bp_week
from blueprints.modul.resource import bp_modul
from blueprints.keyconcept.resource import bp_keyconcept
from blueprints.quiz.resource import bp_quiz
from blueprints.submodul.resource import bp_submodul
from blueprints.category.resource import bp_category
from blueprints.content.resource import bp_content
from blueprints.question.resource import bp_question
from blueprints.choice.resource import bp_choice
from blueprints.auth.resource import bp_auth

app.register_blueprint(bp_user, url_prefix="/user")
app.register_blueprint(bp_course, url_prefix="/course")
app.register_blueprint(bp_week, url_prefix="/week")
app.register_blueprint(bp_modul, url_prefix="/modul")
app.register_blueprint(bp_keyconcept, url_prefix="/keyconcept")
app.register_blueprint(bp_quiz, url_prefix="/quiz")
app.register_blueprint(bp_submodul, url_prefix="/submodul")
app.register_blueprint(bp_category, url_prefix="/category")
app.register_blueprint(bp_content, url_prefix="/content")
app.register_blueprint(bp_question, url_prefix="/question")
app.register_blueprint(bp_choice, url_prefix="/choice")
app.register_blueprint(bp_auth, url_prefix="/auth")

db.create_all()
