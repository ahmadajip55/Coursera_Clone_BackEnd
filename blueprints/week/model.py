from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer

from blueprints.course.model import Courses


class Weeks(db.Model):
    __tablename__ = "weeks"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_id = db.Column(
        db.Integer, db.ForeignKey(Courses.id, ondelete="CASCADE"), nullable=False
    )
    name_week = db.Column(db.String(200), nullable=False)
    duration_week = db.Column(db.Integer, default=7)
    moduls = db.relationship(
        "Moduls", cascade="all, delete-orphan", passive_deletes=True
    )
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "course_id": fields.Integer,
        "name_week": fields.String,
        "duration_week": fields.Integer,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime,
    }

    def __init__(self, course_id, name_week):
        self.course_id = course_id
        self.name_week = name_week

    def __rpr__(self):
        return "<Weeks %r>" % self.id
