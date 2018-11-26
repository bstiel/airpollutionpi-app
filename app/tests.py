import os
import json
import pytz
import sqlalchemy

from datetime import datetime
from unittest import TestCase
from api.models import Timeseries
from app import app, db


class TestTimeseries(TestCase):

    @classmethod
    def setUpClass(cls):
        # drop/create test database
        engine = sqlalchemy.create_engine(os.environ['SQLALCHEMY_DATABASE_URI'])
        connection = engine.connect()
        connection.execute('COMMIT')
        connection.execute('DROP DATABASE IF EXISTS test;')
        connection.execute('COMMIT')
        connection.execute('CREATE DATABASE test;')
        connection.close()

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False

        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI'] + '/test'
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
    def test_can_post(self):
        response = self.app.post('/api/timeseries',
            data=json.dumps([
                {
                    'timestamp': '2018-11-26T15:00:00+00:00',
                    'label': 'raspberry-123',
                    'data': {
                        'temp': 20.1,
                        'humidity': 50.4
                    }
                },
                {
                    'timestamp': '2018-11-26T15:01:00+00:00',
                    'label': 'raspberry-123',
                    'data': {
                        'temp': 20.4,
                        'humidity': 50.1
                    }
                }
            ]),
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(db.session.query(Timeseries).count(), 2)

    def test_can_get(self):
        db.session.add(
            Timeseries(
                timestamp=datetime(2018, 11, 26, 15, 0, 0, 0, pytz.UTC),
                label='raspberry-123',
                data={
                    'temp': 20.1,
                    'humidity': 50.4
                }
            )
        )
        db.session.add(
            Timeseries(
                timestamp=datetime(2018, 11, 26, 15, 1, 0, 0, pytz.UTC),
                label='raspberry-123',
                data={
                    'temp': 20.4,
                    'humidity': 50.1
                }
            )
        )
        db.session.commit()
        response = self.app.get('/api/timeseries')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            [{'data': {'humidity': 50.4, 'temp': 20.1}, 'label': 'raspberry-123', 'timestamp': '2018-11-26T15:00:00+00:00'}, {'data': {'humidity': 50.1, 'temp': 20.4}, 'label': 'raspberry-123', 'timestamp': '2018-11-26T15:01:00+00:00'}]
        )