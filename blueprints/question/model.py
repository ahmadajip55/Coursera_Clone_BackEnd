from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer

from blueprints.quiz.model import Quizs


class Questions(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(
        db.Integer, db.ForeignKey(Quizs.id, ondelete="CASCADE"), nullable=False
    )
    question = db.Column(db.String(2000), nullable=False)
    choice = db.relationship(
        "Choices", cascade="all, delete-orphan", passive_deletes=True
    )
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "quiz_id": fields.Integer,
        "question": fields.String,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime,
    }

    def __init__(self, quiz_id, question):
        self.quiz_id = quiz_id
        self.question = question

    def __rpr__(self):
        return "<Questions %r>" % self.id
