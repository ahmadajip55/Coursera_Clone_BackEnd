from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer

from blueprints.modul.model import Moduls


class Submoduls(db.Model):
    __tablename__ = "submoduls"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    modul_id = db.Column(
        db.Integer, db.ForeignKey(Moduls.id, ondelete="CASCADE"), nullable=False
    )
    name_submodul = db.Column(db.String(200), nullable=False)
    content = db.relationship(
        "Contents", cascade="all, delete-orphan", passive_deletes=True
    )
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "modul_id": fields.Integer,
        "name_submodul": fields.String,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime,
    }

    def __init__(self, modul_id, name_submodul):
        self.modul_id = modul_id
        self.name_submodul = name_submodul

    def __rpr__(self):
        return "<Submoduls %r>" % self.id
