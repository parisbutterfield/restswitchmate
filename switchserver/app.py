import sqlite3 as lite
from os import environ
from flask import Flask, g, request, abort
import manager

DATABASE = '/db/switchmate.db'
LOCAL = "127.0.0.1"


app = Flask(__name__)

def getSharedLocation():
    mainpienv = "MAIN_PISWITCH"
    if mainpienv in environ:
        return environ.get(mainpienv)
    else:
        return LOCAL

sharedAuth = manager.getShared(getSharedLocation()).syncdict()
jobQueue = manager.getShared(LOCAL).get_job_q()

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def myfunc(col):
    val = int(col) == 1
    return val

def get_db():
    db = lite.connect(DATABASE, detect_types=lite.PARSE_DECLTYPES)
    lite.register_converter('boolean', myfunc)
    db.row_factory = make_dicts
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/device/<macaddress>', methods=['PUT'])
def device(macaddress):
    results = None
    newFirmware = request.args.get('newFirmware')
    if newFirmware is None or newFirmware.lower() == 'false':
        try:
            results = sharedAuth.get(macaddress.upper())
            results.update({'newFirmware': False})
        except:
            abort(404)
    elif newFirmware is not None and newFirmware.lower() == 'true':
        results = {}
        results['macaddress'] = macaddress
        results['newFirmware'] = True
    if results != None:
        content = request.get_json(force=True)
        results.update({'on' : content['on']})
        try:
            jobQueue.put(results)
        except:
            abort(404)
        print("Request added to queue")
        return ('', 200)
    abort(404)