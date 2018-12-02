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
        response = self.app.post('/',
            data=json.dumps([
                {
                    'ts': '2018-11-26T15:00:00+00:00',
                    'id': '00:0a:95:9d:68:16',
                    'data': {
                        'temperature': 20.1,
                        'humidity': 50.4
                    }
                },
                {
                    'timestamp': '2018-11-26T15:01:00+00:00',
                    'id': '00:0a:95:9d:68:16',
                    'data': {
                        'temperature': 20.4,
                        'humidity': 50.1
                    }
                }
            ]),
            content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(db.session.query(Timeseries).count(), 2)

    def test_can_get_series(self):
        db.session.add(
            Timeseries(
                timestamp=datetime(2018, 11, 26, 15, 0, 0, 0, pytz.UTC),
                id='00:0a:95:9d:68:16',
                data={
                    'temperature': 20.1,
                    'humidity': 50.4
                }
            )
        )
        db.session.add(
            Timeseries(
                timestamp=datetime(2018, 11, 26, 15, 1, 0, 0, pytz.UTC),
                id='00:0a:95:9d:68:16',
                data={
                    'humidity': 50.1
                }
            )
        )
        db.session.add(
            Timeseries(
                timestamp=datetime(2018, 11, 27, 10, 1, 0, 0, pytz.UTC),
                id='00-06:5b-bc-7a-c7',
                data={
                    'temperature': 17.4,
                    'humidity': 43.1
                }
            )
        )
        db.session.commit()
        response = self.app.get('/series?id=00:0a:95:9d:68:16')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            [
                {'id': '00:0a:95:9d:68:16', 'series': 'humidity'},
                {'id': '00:0a:95:9d:68:16', 'series': 'temperature'}
            ]
        )

    def test_can_get_timeseries(self):
        db.session.add(
            Timeseries(
                timestamp=datetime(2018, 11, 26, 15, 0, 0, 0, pytz.UTC),
                id='00:0a:95:9d:68:16',
                data={
                    'temperature': 20.1,
                    'humidity': 50.4
                }
            )
        )
        db.session.add(
            Timeseries(
                timestamp=datetime(2018, 11, 26, 15, 1, 0, 0, pytz.UTC),
                id='00:0a:95:9d:68:16',
                data={
                    'humidity': 50.1
                }
            )
        )
        db.session.add(
            Timeseries(
                timestamp=datetime(2018, 11, 27, 10, 1, 0, 0, pytz.UTC),
                id='00-06:5b-bc-7a-c7',
                data={
                    'temperature': 17.4,
                    'humidity': 43.1
                }
            )
        )
        db.session.commit()
        response = self.app.get('/00:0a:95:9d:68:16/temperature')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            [{'t': '2018-11-26T15:00:00+00:00', 'v': 20.1}]
        )