from __future__ import print_function
import os
import sys
import struct
import ctypes
import time
import threading
import manager

from netaddr import EUI
import netaddr
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, ADDR_TYPE_RANDOM
from binascii import unhexlify

SWITCHMATE_SERVICE = '23d1bcea5f782315deef121223150000'
NOTIFY_VALUE = struct.pack('<BB', 0x01, 0x00)

STATE_HANDLE = 0x000e
STATE_NOTIFY_HANDLE = 0x000f
NEW_STATE_HANDLE = 0x30
LOCAL = "127.0.0.1"

def c_mul(a, b):
	'''
	Multiplication function with overflow
	'''
	return ctypes.c_int64((long(a) * b) &0xffffffffffffffff).value

def sign(data, key):
	'''
	Variant of the Fowler-Noll-Vo (FNV) hash function
	'''
	blob = data + key
	x = ord(blob[0]) << 7
	for c in blob:
		x1 = c_mul(1000003, x)
		x = x1 ^ ord(c) ^ len(blob)

	# once we have the hash, we append the data
	shifted_hash = (x & 0xffffffff) << 16
	shifted_data_0 = ord(data[0]) << 48
	shifted_data_1 = ord(data[1]) << 56
	packed = struct.pack('<Q', shifted_hash | shifted_data_0 | shifted_data_1)[2:]
	return packed



class NotificationDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, handle, data):
        if ord(data[-1]) == 0:
            print('Switched!')
        else:
            print('Switching failed!')

class BackgroundThread(object):

    @staticmethod
    def convertMac(macaddress):
        mac = EUI(macaddress)
        mac.dialect = netaddr.mac_unix_expanded
        return str(mac)

    def __init__(self, interval=2):

        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = False
        thread.start()  # Start the execution

    def run(self):
        switchqueue = manager.getShared(LOCAL).get_job_q()
        while True:
            if not switchqueue.empty():
                try:
                    item = switchqueue.get()
                    switch = item['on']
                    if switch:
                        val = '\x01'
                    else:
                        val = '\x00'
                    macaddress = self.convertMac(item['macaddress'])
                    device = Peripheral(macaddress, ADDR_TYPE_RANDOM,int(os.environ['SCAN_HCI']))
                    if item['newFirmware'] is False:
                      notifications = NotificationDelegate()
                      device.setDelegate(notifications)
                      auth_key = unhexlify(item['authkey'])
                      device.writeCharacteristic(STATE_NOTIFY_HANDLE, NOTIFY_VALUE, True)
                      device.writeCharacteristic(STATE_HANDLE, sign('\x01' + val, auth_key))
                      while True:
                          if device.waitForNotifications(1.0):
                              device.disconnect()
                              print('Ending session')
                              break
                          print('Waiting for notification. Old Firmware.')
                    else: # new firmware. No notifcation and no auth
                        device.writeCharacteristic(NEW_STATE_HANDLE, val, True)
                    device.disconnect()
                except Exception as e:
                    print(e)
            time.sleep(1);

def myfunc(col):
    val = int(col) == 1
    return val


BackgroundThread()
print('Switchmate SwitchServer Running')
