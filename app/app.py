import sys
import logging
import time
import logging
import json
import os
import dateutil.parser

from datetime import datetime
from functools import wraps
from uuid import uuid4 as uuid
from logging.config import dictConfig
from flask import jsonify, request, g
from api import app, db
from api.models import Timeseries


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
})


logger = app.logger


@app.route('/', methods=['POST'])
def index():
    # generic data sink
    for i in request.json:
        db.session.add(Timeseries(
            id=i['id'],
            timestamp=dateutil.parser.parse(i.get('timestamp', i.get('ts'))),
            latitude=i.get('latitude'),
            longitude=i.get('longitude'),
            elevation=i.get('elevation'),
            speed=i.get('speed'),
            data=i['data']
        ))
    db.session.commit()
    return '', 201


@app.route('/series', methods=['GET'])
def series():
    if 'id' in request.args:
        result = db.session.execute("SELECT DISTINCT id, series FROM (SELECT id, jsonb_object_keys(timeseries.data) AS series FROM timeseries WHERE timeseries.id=:id) AS q ORDER BY series, id ASC;", {'id': request.args['id']})
    else:
        result = db.session.execute("SELECT DISTINCT id, jsonb_object_keys(timeseries.data) AS series FROM timeseries ORDER BY series, id ASC;")
    return jsonify([dict(id=i[0], series=i[1]) for i in result])


@app.route('/<string:id>/<string:series>', methods=['GET'])
def timeseries(id, series):
    # return timeseries
    data = db.session\
        .query(Timeseries)\
        .filter(Timeseries.id==id)\
        .filter(Timeseries.data.has_key(series))\
        .filter_by(**request.args)\
        .order_by(Timeseries.timestamp)
    return jsonify([
        {
            't': i.timestamp.isoformat(),
            'p': (i.latitude, i.longitude),
            'e': i.elevation,
            's': i.speed,
            'v': i.data[series]
        } for i in data]), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)