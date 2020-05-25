from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer


class Courses(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_course = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(2000))
    weeks = db.relationship("Weeks", cascade="all, delete-orphan", passive_deletes=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "name_course": fields.String,
        "description": fields.String,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime,
    }

    def __init__(self, name_course, description):
        self.name_course = name_course
        self.description = description

    def __rpr__(self):
        return "<Courses %r>" % self.id
