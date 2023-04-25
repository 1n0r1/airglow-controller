import time
import serial
from time import sleep
import logging


class FilterWheel():
    ser = None
    def __init__(self, port):
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
        except:
            print("Can't open serial port")
        logging.info('Initialized FilterWheel')

    def home(self):
        try:
            self.ser.write('home\n'.encode())
            sleep(10)
            res = self.ser.readline()
            logging.info('FilterWheel response: ' + res.decode())
        except:
            logging.error('Cannot write to FilterWheel')

    def go(self, position):
        try:
            self.ser.write(f'go{position}\n'.encode())
            sleep(10)
            res = self.ser.readline()
            logging.info('FilterWheel response: ' + res.decode())
        except:
            logging.error('Cannot write to FilterWheel')