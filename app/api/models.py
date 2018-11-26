from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates, backref
from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import JSONB
from . import db


class Timeseries(db.Model):
    __tablename__ = 'timeseries'
    timestamp = db.Column(db.DateTime(timezone=True), primary_key=True, unique=False, nullable=False)
    label = db.Column(db.String(64), primary_key=True, unique=False, nullable=False)
    data = db.Column(JSONB, nullable=False)
