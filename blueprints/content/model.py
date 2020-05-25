from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer

from blueprints.submodul.model import Submoduls
from blueprints.category.model import Categories


class Contents(db.Model):
    __tablename__ = "contents"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    submodul_id = db.Column(
        db.Integer, db.ForeignKey(Submoduls.id, ondelete="CASCADE"), nullable=False
    )
    category_id = db.Column(
        db.Integer, db.ForeignKey(Categories.id, ondelete="CASCADE"), nullable=False
    )
    name_content = db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "submodul_id": fields.Integer,
        "category_id": fields.Integer,
        "name_content": fields.String,
        "content": fields.String,
        "description": fields.String,
        "duration": fields.Integer,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime,
    }

    def __init__(
        self, submodul_id, category_id, name_content, content, description, duration
    ):
        self.submodul_id = submodul_id
        self.category_id = category_id
        self.name_content = name_content
        self.content = content
        self.description = description
        self.duration = duration

    def __rpr__(self):
        return "<Contents %r>" % self.id
