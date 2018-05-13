import sqlite3 as lite
import sys
import manager 

DATABASE = '/db/switchmate.db'


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

results = query_db('select * from Auth', [], one=False)
for result in results:
    insert = {result['macaddress'] : result}
    print "Updating into Shared Dict"
    print insert
    manager.getShared("127.0.0.1").syncdict().update(insert)