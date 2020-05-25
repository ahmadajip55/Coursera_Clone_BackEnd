from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer


class Categories(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_category = db.Column(db.String(200), nullable=False)
    content = db.relationship(
        "Contents", cascade="all, delete-orphan", passive_deletes=True
    )
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "name_category": fields.String,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime,
    }

    def __init__(self, name_category):
        self.name_category = name_category

    def __rpr__(self):
        return "<Category %r>" % self.id
