from blueprints import db
from flask_restful import fields
from sqlalchemy import func
from sqlalchemy.sql.expression import text
from datetime import datetime

from sqlalchemy import Table, Column, Integer


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    pin = db.Column(db.String(255), nullable=False)
    place_birth = db.Column(db.String(200), nullable=False)
    date_birth = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

    response_fields = {
        "id": fields.Integer,
        "username": fields.String,
        "full_name": fields.String,
        "place_birth": fields.String,
        "date_birth": fields.String,
        "address": fields.String,
        "created_at": fields.DateTime,
        "update_at": fields.DateTime,
    }

    jwt_claims_fields = {
        "id": fields.Integer,
        "username": fields.String,
        "full_name": fields.String,
    }

    def __init__(self, username, full_name, pin, place_birth, date_birth, address):
        self.username = username
        self.full_name = full_name
        self.place_birth = place_birth
        self.date_birth = date_birth
        self.address = address

    def __rpr__(self):
        return "<Users %r>" % self.id
