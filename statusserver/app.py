import sqlite3 as lite
import json
from flask import Flask, g, abort, render_template
from flask_cors import CORS


class FlaskAppWrapper(object):
    DATABASE = '/db/switchmate.db'

    app = Flask(__name__)
    CORS(app)

    def __init__(self):
        app = Flask(__name__)

    def run(self):
        self.app.run(host="0.0.0.0", debug=False)

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

    @staticmethod
    @app.route('/devices')
    def devices():
        results = FlaskAppWrapper.query_db('select * from Switchmate')
        return json.dumps(results)

    @app.route('/device/<macaddress>')
    def device(macaddress):
        results = FlaskAppWrapper.query_db('select * from Switchmate where macaddress = ?', (macaddress.upper(),),
                                           one=True)
        if results != None:
            return json.dumps(results)
        abort(404)

    @app.route('/device/<macaddress>/status')
    def devicestatus(macaddress):
        results = FlaskAppWrapper.query_db('select status from Switchmate where macaddress = ?', (macaddress.upper(),),
                                           one=True)
        if results != None:
            return json.dumps(results)
        abort(404)

    @app.route("/status")
    def index():
        return render_template('index.html')