from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates, backref
from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import JSONB
from . import db


class Timeseries(db.Model):
    __tablename__ = 'timeseries'
    id = db.Column(db.String(128), primary_key=True, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), primary_key=True, nullable=False)
    latitude = db.Column(db.Float(), nullable=True)
    longitude = db.Column(db.Float(), nullable=True)
    elevation = db.Column(db.Float(), nullable=True)
    speed = db.Column(db.Float(), nullable=True)
    data = db.Column(JSONB, nullable=False)
