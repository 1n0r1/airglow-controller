import time
import serial
from time import sleep



class LaserShutter():
    ser = None

    def __init__(self):
        try:
            self.ser = serial.Serial(
                port='/dev/ttyACM1',
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
            )
        except :
            print("Can't open serial port")

    def open_shutter(self):
        self.close_shutter()
        self.ser.write('open\n'.encode())
        sleep(2)
        res=self.ser.readline()
        print(res.decode())

    def close_shutter(self):
        self.ser.write('close\n'.encode())
        sleep(2)
        res=self.ser.readline()
        print(res.decode())

