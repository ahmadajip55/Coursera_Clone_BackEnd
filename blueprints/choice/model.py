from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer

from blueprints.question.model import Questions


class Choices(db.Model):
    __tablename__ = "choices"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(
        db.Integer, db.ForeignKey(Questions.id, ondelete="CASCADE"), nullable=False
    )
    choice = db.Column(db.String(2000), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "question_id": fields.Integer,
        "choice": fields.String,
        "status": fields.Boolean,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime,
    }

    def __init__(self, question_id, choice, status):
        self.question_id = question_id
        self.choice = choice
        self.status = status

    def __rpr__(self):
        return "<Choices %r>" % self.id
