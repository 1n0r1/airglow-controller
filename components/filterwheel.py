import time
import requests
import serial
from time import sleep
import logging


class FilterWheel():
    ser = None
    ip_address = None
    def __init__(self, ip_address=None, port=None):
        # ip_address = 'http://192.168.1.143:8080/'
        if port != None:
            try:
                self.ser = serial.Serial(
                    port=port,
                    baudrate=9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    bytesize=serial.EIGHTBITS,
                    write_timeout = 1,
                    timeout=1
                )
                logging.info('Initialized FilterWheel')
            except:
                print("Can't open serial port")
            return
        if ip_address != None:
            try:
                self.ip_address = ip_address
                logging.info('Initialized FilterWheel')
                text = requests.get(url=self.ip_address, timeout=100).text
                logging.info('FilterWheel response: ' + text)
            except:
                print("Can't open serial port")

    def home(self):
        if self.ser != None:
            try:
                self.ser.write('home\n'.encode())
                sleep(10)
                res = self.ser.readline()
                logging.info('FilterWheel response: ' + res.decode())
            except:
                logging.error('Cannot write to FilterWheel')
            return
        if self.ip_address != None:
            text = requests.get(url=self.ip_address + 'home', timeout=100).text
            logging.info('FilterWheel response: ' + text)
        
    def go(self, position):
        if self.ser != None:
            try:
                self.ser.write(f'go{position}\n'.encode())
                sleep(10)
                res = self.ser.readline()
                logging.info('FilterWheel response: ' + res.decode())
            except:
                logging.error('Cannot write to FilterWheel')
            return
        if self.ip_address != None:
            text = requests.get(url=self.ip_address + f'go/{position}', timeout=100).text
            logging.info('FilterWheel response: ' + text)
