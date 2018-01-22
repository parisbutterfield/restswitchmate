
import struct

from bluepy.btle import Scanner, DefaultDelegate, Peripheral, ADDR_TYPE_RANDOM
from binascii import hexlify
from netaddr import EUI
import netaddr
import time
from queue import statusqueue, authqueue
import datetime
import os
import sqlite3 as lite



SWITCHMATE_SERVICE = '23d1bcea5f782315deef121223150000'
NOTIFY_VALUE = struct.pack('<BB', 0x01, 0x00)

AUTH_NOTIFY_HANDLE = 0x0017
AUTH_HANDLE = 0x0016
AUTH_INIT_VALUE = struct.pack('<BBBBBB', 0x00, 0x00, 0x00, 0x00, 0x01, 0x00)

DATABASE = '../db/switchmate.db'



class NotificationDelegate(DefaultDelegate):
    def __init__(self, macaddress):
        DefaultDelegate.__init__(self)
        self.con = lite.connect(DATABASE)
        self.macaddress = macaddress

    @staticmethod
    def convertMac(macaddress):
        mac = EUI(macaddress)
        mac.dialect = netaddr.mac_bare
        return str(mac)

    def handleNotification(self,  handle, data):
        if handle == AUTH_HANDLE:
            key=hexlify(data[3:]).upper()
            if not key:
              print("Unable to get key. Please try again.")
            else:
              statusqueue.put( 'Auth key is {}'.format(key))
              sql = ''' INSERT OR REPLACE INTO Auth(macaddress, authkey, updated) 
              				      VALUES (?, ?, ?) '''
              data = (self.convertMac(self.macaddress), key, datetime.datetime.now())
              print('inserting data: ', data)
              cur = self.con.cursor()
              cur.execute(sql, data)
              self.con.commit()
              statusqueue.put('Auth key has been saved')

class AuthSession:
    @staticmethod
    def convertMac(macaddress):
        mac = EUI(macaddress)
        mac.dialect = netaddr.mac_unix_expanded
        return str(mac)

    def __init__(self, macaddress):
        self.macaddress = self.convertMac(macaddress)
        statusqueue.put("Starting auth for "+ macaddress)


    def start(self):
        try:
            device = Peripheral(self.macaddress, ADDR_TYPE_RANDOM, int(os.environ['SCAN_HCI']))
            notifications = NotificationDelegate(self.macaddress)
            device.setDelegate(notifications)
            device.writeCharacteristic(AUTH_NOTIFY_HANDLE, NOTIFY_VALUE, True)
            device.writeCharacteristic(AUTH_HANDLE, AUTH_INIT_VALUE, True)
            print('Press button')
            statusqueue.put('Press button on Switchmate to get auth key')
            while True:
                if device.waitForNotifications(1.0):
                    statusqueue.put('Ending session')
                    break
                statusqueue.put('Waiting for notification')
                time.sleep(0)
            device.disconnect()
        except Exception as e:
            print(e)
