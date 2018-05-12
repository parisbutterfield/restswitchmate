from __future__ import print_function
import struct
import os
import sys
import threading
import time
import datetime
import sqlite3 as lite
from netaddr import EUI
import netaddr

from bluepy.btle import Scanner, DefaultDelegate, Peripheral, ADDR_TYPE_RANDOM

# firmware < 2.99.15
OLD_FIRMWARE_SERVICE = '23d1bcea5f782315deef121223150000'
# firmware == 2.99.15 (or higher?)
NEW_FIRMWARE_SERVICE = 'abd0f555eb40e7b2ac49ddeb83d32ba2'

SWITCHMATE_SERVICES = [
    OLD_FIRMWARE_SERVICE,
    NEW_FIRMWARE_SERVICE,
]

NOTIFY_VALUE = struct.pack('<BB', 0x01, 0x00)



STATE_HANDLE = 0x000e
STATE_NOTIFY_HANDLE = 0x000f

NEW_STATE_HANDLE = 0x30

SERVICES_AD_TYPE = 0x07

DATABASE = '/db/switchmate.db'

def noop(x):
    return x

if sys.version_info >= (3,):
    long = int
    ord = noop

def insertDBRecord(data):
    print(data)
    con = lite.connect(DATABASE)
    sql = ''' INSERT OR REPLACE INTO Switchmate(macaddress, status, updated)
    				      VALUES (?, ?, ?) '''

    cur = con.cursor()
    cur.execute(sql, data)
    con.commit()

def convertMac(macaddress):
    mac = EUI(macaddress)
    mac.dialect = netaddr.mac_bare
    return str(mac)

def readnewFirmware(macaddress):
    try:
        peripheral = Peripheral(macaddress, ADDR_TYPE_RANDOM)
        val = ord(peripheral.readCharacteristic(NEW_STATE_HANDLE))
        data = (convertMac(macaddress), (False, True)[val], datetime.datetime.now())
        insertDBRecord(data)
        peripheral.disconnect()
    except Exception as ex:
        print('WARNING: Could not read status of {}. {}'.format(macaddress, ex.message))


class ScanDelegate(DefaultDelegate):
    def __init__(self, set):
        DefaultDelegate.__init__(self)
        self.seen = []
        self.set = set

    def handleDiscovery(self, dev, isNewDev, isNewData):

        if dev.addr in self.seen:
            return
        self.seen.append(dev.addr)

        AD_TYPE_SERVICE_DATA = 0x16
        NEW_DATA = 30
        service = dev.getValueText(SERVICES_AD_TYPE)
        val = None
        if service == OLD_FIRMWARE_SERVICE:
            data = dev.getValueText(AD_TYPE_SERVICE_DATA)
            # the bit at 0x0100 signifies if the switch is off or on
            val = (int(data, 16) >> 8) & 1
        elif service == NEW_FIRMWARE_SERVICE:
            self.set.add(dev.addr)

        if val is not None:
            data = (convertMac(dev.addr), (False, True)[val], datetime.datetime.now())
            insertDBRecord(data)


class BackgroundThread(object):

    def __init__(self):

        self.interval = int(os.environ['SCAN_INTERVAL'])
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = False
        thread.start()  # Start the execution

    def run(self):
        while True:
            # Do something
            print('Starting Scan Process')
            items = set()
            scanner = Scanner().withDelegate(ScanDelegate(items))
            scanner.clear()
            scanner.start()
            scanner.process(5)
            scanner.stop()
            for item in items:
                readnewFirmware(item)
            time.sleep(self.interval)
	sys.exit() #If the loop exists because of an error, let the process go down and have docker restart it.

def myfunc(col):
    val = int(col) == 1
    return val


con = lite.connect(DATABASE, detect_types=lite.PARSE_DECLTYPES)
lite.register_converter('boolean', myfunc)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Switchmate (macaddress TEXT PRIMARY KEY, status boolean, updated INT)")
BackgroundThread()
print('Switchmate Scan Running')
