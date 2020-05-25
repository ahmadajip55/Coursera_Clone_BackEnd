from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer

from blueprints.modul.model import Moduls


class Quizs(db.Model):
    __tablename__ = "quizs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    modul_id = db.Column(
        db.Integer, db.ForeignKey(Moduls.id, ondelete="CASCADE"), nullable=False
    )
    name_quiz = db.Column(db.String(200), nullable=False)
    duration_minute = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    question = db.relationship(
        "Questions", cascade="all, delete-orphan", passive_deletes=True
    )
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "modul_id": fields.Integer,
        "name_quiz": fields.String,
        "duration_minute": fields.Integer,
        "grade": fields.Integer,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime,
    }

    def __init__(self, modul_id, name_quiz, duration_minute, grade):
        self.modul_id = modul_id
        self.name_quiz = name_quiz
        self.duration_minute = duration_minute
        self.grade = grade

    def __rpr__(self):
        return "<Quizs %r>" % self.id
