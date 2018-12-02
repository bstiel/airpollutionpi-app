from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, validates, backref
from sqlalchemy import ForeignKey, text
from sqlalchemy.dialects.postgresql import JSONB
from . import db


class Timeseries(db.Model):
    __tablename__ = 'timeseries'
    timestamp = db.Column(db.DateTime(timezone=True), primary_key=True, nullable=False)
    id = db.Column(db.String(128), primary_key=True, nullable=False)
    data = db.Column(JSONB, nullable=False)
