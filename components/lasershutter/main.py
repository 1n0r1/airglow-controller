import time
import serial
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import logging
from datetime import datetime

logging.basicConfig(filename='/home/airglow/airglow_shutter_controller/logs/' + datetime.now().strftime('_%Y%m%d_%H%M%S.log'), 
                    format='%(asctime)s %(message)s', 
                    encoding='utf-8', 
                    level=logging.DEBUG)
                    
logging.info('Listener start')

kit = MotorKit(i2c=board.I2C())

ser = serial.Serial(
    port='/dev/ttyGS0',
    baudrate = 9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=60 #log every 1 min
)

logging.info('USB communication normal')

while 1:
    x = ser.readline()
    req = x.decode()
    logging.info('Read ' + str(x))
    if req == "open\n":
        logging.info('Opening')
        kit.stepper1.release()
        for i in range(7):
            kit.stepper1.onestep(style=stepper.DOUBLE)
            time.sleep(0.2)
        logging.info('Opened')
        ser.write("opened\n".encode())
    if req == "close\n":
        logging.info('Closing')
        kit.stepper1.release()
        logging.info('Closed')
        ser.write("closed\n".encode())