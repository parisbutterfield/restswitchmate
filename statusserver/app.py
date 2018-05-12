import sqlite3 as lite
import json
import requests
import threading
from urlparse import urlparse
from flask import Flask, g, abort, render_template, request
from flask_cors import CORS
app = Flask(__name__)
DATABASE = '/db/switchmate.db'


if __name__ == "__main__":
    app.run(host='0.0.0.0')
    CORS(app)

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def myfunc(col):
    val = int(col) == 1
    return val

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = lite.connect(DATABASE, detect_types=lite.PARSE_DECLTYPES)
        lite.register_converter('boolean', myfunc)
        db.row_factory = make_dicts
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@staticmethod
@app.route('/devices')
def devices():
    results = query_db('select * from Switchmate')
    return json.dumps(results)

@app.route('/device/<macaddress>' , methods=['GET'])
def device(macaddress):
    results = query_db('select * from Switchmate where macaddress = ?', (macaddress.upper(),),
                                       one=True)
    if results != None:
        return json.dumps(results)
    abort(404)

@app.route('/device/<macaddress>/status')
def devicestatus(macaddress):
    results = query_db('select status from Switchmate where macaddress = ?', (macaddress.upper(),),
                                       one=True)
    if results != None:
        return json.dumps(results)
    abort(404)

@app.route("/status")
def index():
    return render_template('index.html')
