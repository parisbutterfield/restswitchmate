import sqlite3 as lite
import json
import requests
from os import environ
from flask import Flask, g, request, abort
from flask_cors import CORS
from queue import switchqueue

class FlaskAppWrapper(object):
    DATABASE = '/db/switchmate.db'

    app = Flask(__name__)
    CORS(app)

    def __init__(self):
        app = Flask(__name__)

    def run(self):
        self.app.run(host="0.0.0.0", port=5002)

    @staticmethod
    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value)
                    for idx, value in enumerate(row))

    @staticmethod
    def myfunc(col):
        val = int(col) == 1
        return val

    @staticmethod
    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = lite.connect(FlaskAppWrapper.DATABASE, detect_types=lite.PARSE_DECLTYPES)
            lite.register_converter('boolean', FlaskAppWrapper.myfunc)
            db.row_factory = FlaskAppWrapper.make_dicts
        return db

    @staticmethod
    def query_db(query, args=(), one=False):
        cur = FlaskAppWrapper.get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

    @app.route('/device/relay/<macaddress>', methods=['PUT'])
    def device(macaddress):
        content = request.get_json(force=True)
        print(content)
        switchqueue.put(content);
        print("Adding relayed request to queue")
        return ('', 200)
    abort(404)

    @app.route('/device/<macaddress>', methods=['PUT'])
    def device(macaddress):
        results = FlaskAppWrapper.query_db('select * from Switchmate INNER JOIN Auth ON Auth.macaddress = Switchmate.macaddress where Switchmate.macaddress = ?', (macaddress.upper(),),
                                           one=True)
        if results != None:
            content = request.get_json(force=True)
            results.update({'on' : content['on']})
            if macaddress in os.environ:
                print("Relaying request...")
                host = environ.get(macaddress)
                r = requests.put("http://" + host + ":5002/device/relay/" + macaddress, data = json.dumps(results))
            else
                switchqueue.put(results);
                print("Request added to queue")
        return ('', 200)
        abort(404)
