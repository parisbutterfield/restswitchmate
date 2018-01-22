import Queue
from flask_socketio import SocketIO, emit
from flask import Flask, g, abort
from queue import statusqueue, authqueue
import sqlite3 as lite

count = 0

def background_status_thread():
    print("Status Background Thread Listening")
    while count > 0:
        if not statusqueue.empty():
            item = statusqueue.get()
            print('Sending item ' + item)
            socketio.emit('status', item)
        socketio.sleep(0)
    print("Status Background Thread has stopped")

def background_auth_thread():
    from auth import AuthSession
    print("Auth Background Thread Listening")
    while count > 0:
        if not authqueue.empty():
            item = authqueue.get()
            auth = AuthSession(item)
            auth.start()
        socketio.sleep(0)
    print("Auth Background Thread has stopped")



fapp = Flask(__name__)
socketio = SocketIO(fapp)

@socketio.on('auth')
def handle_auth(macaddress):
    print("Got auth request for: " + macaddress)
    authqueue.put(macaddress)

#We only allow one client to connect here. Other clients will be rejected.
@socketio.on('connect')
def connect():
    global count
    if count == 0:
        count += 1
        socketio.start_background_task(target=background_status_thread)
        socketio.start_background_task(target=background_auth_thread)

        emit('status', 'Connected to Server')
    else:
       return False

#On disconnect we kill the background threads though the use of the global count variable
@socketio.on('disconnect')
def disconnect():
    global count
    count -= 1


con = lite.connect('../db/switchmate.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Auth (macaddress TEXT PRIMARY KEY, authkey TEXT, updated INT)")
socketio.run(fapp, '0.0.0.0', port=5001, debug=True)
