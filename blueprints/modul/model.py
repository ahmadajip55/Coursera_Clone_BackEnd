from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer

from blueprints.week.model import Weeks


class Moduls(db.Model):
    __tablename__ = "moduls"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    week_id = db.Column(
        db.Integer, db.ForeignKey(Weeks.id, ondelete="CASCADE"), nullable=False
    )
    name_modul = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    keyconcept = db.relationship(
        "KeyConcepts", cascade="all, delete-orphan", passive_deletes=True
    )
    quiz = db.relationship("Quizs", cascade="all, delete-orphan", passive_deletes=True)
    submodul = db.relationship(
        "Submoduls", cascade="all, delete-orphan", passive_deletes=True
    )
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "week_id": fields.Integer,
        "name_modul": fields.String,
        "description": fields.String,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime,
    }

    def __init__(self, week_id, name_modul, description):
        self.week_id = week_id
        self.name_modul = name_modul
        self.description = description

    def __rpr__(self):
        return "<Moduls %r>" % self.id
