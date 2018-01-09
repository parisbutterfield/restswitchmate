from __future__ import print_function
import struct
import os
import ctypes
import threading
import time
import datetime
import sqlite3 as lite
from netaddr import EUI
import netaddr

from bluepy.btle import Scanner, DefaultDelegate, Peripheral, ADDR_TYPE_RANDOM
from app import FlaskAppWrapper

SWITCHMATE_SERVICE = '23d1bcea5f782315deef121223150000'
NOTIFY_VALUE = struct.pack('<BB', 0x01, 0x00)

AUTH_NOTIFY_HANDLE = 0x0017
AUTH_HANDLE = 0x0016
AUTH_INIT_VALUE = struct.pack('<BBBBBB', 0x00, 0x00, 0x00, 0x00, 0x01, 0x00)

STATE_HANDLE = 0x000e
STATE_NOTIFY_HANDLE = 0x000f


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.seen = []
        self.con = lite.connect('switchmate.db')

    @staticmethod
    def convertMac(macaddress):
        mac = EUI(macaddress)
        mac.dialect = netaddr.mac_bare
        return str(mac)

    def handleDiscovery(self, dev, isNewDev, isNewData):

        if dev.addr in self.seen:
            return
        self.seen.append(dev.addr)

        AD_TYPE_UUID = 0x07
        AD_TYPE_SERVICE_DATA = 0x16
        if dev.getValueText(AD_TYPE_UUID) == SWITCHMATE_SERVICE:
            data = dev.getValueText(AD_TYPE_SERVICE_DATA)
            # the bit at 0x0100 signifies if the switch is off or on
            sql = ''' INSERT OR REPLACE INTO Switchmate(macaddress, status, updated) 
				      VALUES (?, ?, ?) '''
            data = (self.convertMac(dev.addr), (False, True)[(int(data, 16) >> 8) & 1], datetime.datetime.now())
            print('inserting data: ', data)
            cur = self.con.cursor()
            cur.execute(sql, data)
            self.con.commit()


class BackgroundThread(object):

    def __init__(self, interval=2):

        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = False
        thread.start()  # Start the execution

    def run(self):
        while True:
            # Do something
            print('Starting Scan Process')
            scanner = Scanner(int(os.environ['SCAN_HCI'])).withDelegate(ScanDelegate())
            scanner.clear()
            scanner.start()
            scanner.process(5)
            scanner.stop()
            time.sleep(self.interval)

class FlaskThread(object):

    def __init__(self):

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = False
        thread.start()  # Start the execution

    def run(self):
        app = FlaskAppWrapper()
        app.run()
        print('Staring Scan REST API')

def myfunc(col):
    val = int(col) == 1
    return val


con = lite.connect('switchmate.db', detect_types=lite.PARSE_DECLTYPES)
lite.register_converter('boolean', myfunc)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Switchmate (macaddress TEXT PRIMARY KEY, status boolean, updated INT)")
BackgroundThread()
print('Switchmate Scan Running')
FlaskThread()
