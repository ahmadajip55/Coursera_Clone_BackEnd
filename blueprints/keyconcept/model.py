from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer

from blueprints.modul.model import Moduls


class KeyConcepts(db.Model):
    __tablename__ = "keyconcepts"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    modul_id = db.Column(
        db.Integer, db.ForeignKey(Moduls.id, ondelete="CASCADE"), nullable=False
    )
    concept = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "modul_id": fields.Integer,
        "concept": fields.String,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime,
    }

    def __init__(self, modul_id, concept):
        self.modul_id = modul_id
        self.concept = concept

    def __rpr__(self):
        return "<KeyConcepts %r>" % self.id
