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


@app.route('/api/timeseries', methods=['POST', 'GET'])
def timeseries():
    if request.method == 'POST':
        for i in request.json:
            db.session.add(Timeseries(
                timestamp=dateutil.parser.parse(i['timestamp']),
                label=i['label'],
                data=i['data']
            ))
        db.session.commit()
        return '', 201
    
    data = db.session.query(Timeseries).filter_by(**request.args)
    return jsonify([{
        'timestamp': i.timestamp.isoformat(),
        'label': i.label,
        'data': i.data
    } for i in data]), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)