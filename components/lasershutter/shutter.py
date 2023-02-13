import time
import serial
from time import sleep
import logging


class LaserShutter():
    ser = None
    def __init__(self):
        try:
            self.ser = serial.Serial(
                port='/dev/ttyACM0',
                baudrate=9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                write_timeout = 1,
                timeout=1
            )
        except:
            print("Can't open serial port")
        logging.info('Initialized LaserShutter')

    def open_shutter(self):
        try:
            self.close_shutter()
            self.ser.write('open\n'.encode())
            sleep(2)
            res = self.ser.readline()
            print(res.decode())
            logging.info('LaserShutter response: ' + res.decode())
        except:
            logging.error('Cannot write to LaserShutter')

    def close_shutter(self):
        try:
            self.ser.write('close\n'.encode())
            sleep(2)
            res = self.ser.readline()
            print(res.decode())
            logging.info('LaserShutter response: ' + res.decode())
        except:
            logging.error('Cannot write to LaserShutter')
