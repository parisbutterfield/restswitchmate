from __future__ import print_function
import sys
import struct
import ctypes
import time
import threading

from netaddr import EUI
import netaddr
from queue import switchqueue

from bluepy.btle import Scanner, DefaultDelegate, Peripheral, ADDR_TYPE_RANDOM
from binascii import unhexlify

from app import FlaskAppWrapper

SWITCHMATE_SERVICE = '23d1bcea5f782315deef121223150000'
NOTIFY_VALUE = struct.pack('<BB', 0x01, 0x00)

STATE_HANDLE = 0x000e
STATE_NOTIFY_HANDLE = 0x000f

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
        while True:
            if not switchqueue.empty():
                try:
                    item = switchqueue.get()
                    switch = item['on']
                    macaddress = self.convertMac(item['macaddress'])
                    auth_key  = unhexlify(item ['authkey'])
                    notifications = NotificationDelegate()
                    device = Peripheral(macaddress, ADDR_TYPE_RANDOM,int(os.environ['SCAN_HCI']))
                    device.setDelegate(notifications)
                    device.writeCharacteristic(STATE_NOTIFY_HANDLE, NOTIFY_VALUE, True)
                    device.writeCharacteristic(STATE_HANDLE, sign('\x01' + ('\x00', '\x01')[switch], auth_key))
                    while True:
                        if device.waitForNotifications(1.0):
                            print('Ending session')
                            break
                        print('Waiting for notification')
                    device.disconnect()
                except Exception as e:
                    print(e)
            time.sleep(1);

class FlaskThread(object):

    def __init__(self):

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = False
        thread.start()  # Start the execution

    def run(self):
        app = FlaskAppWrapper()
        app.run()

def myfunc(col):
    val = int(col) == 1
    return val


BackgroundThread()
FlaskThread()
print('Switchmate SwitchServer Running')
