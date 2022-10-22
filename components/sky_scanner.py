#from distutils.command.config import config
#from multiprocessing.sharedctypes import Value
#from pickle import NONE
import serial
#import config.py

# class SkyScanner highlighting the different 
"""The SkyScanner class consists of methods to help operate the SkyScanner in an efficient and effective way."""

class SkyScanner():
    ser = None
    # max_steps = None
    # all in the lfongi file
    # the locaqtion of the sun 
    # azmith offset
    # zenith offset
    # number of steps
    
    def __init__(self):
        # max_steps = MaxSteps
        # self._setSmartMotorVariables()
        try:
            self._openSerial()
        except :
            print("Can't open serial port")
           #
        # finally:
        #     self._closeSerial()

    def set_pos_azi(self, azi_machine_step):
        strr = 'a=%d '% azi_machine_step
        self.ser.write(strr.encode())
        self.ser.write('GOSUB4 '.encode())
        # return azi

    def set_pos_zeni(self, zeni_machine_step):
        strr = 'z=%d ' %zeni_machine_step
        self.ser.write(strr.encode())
        self.ser.write('GOSUB4 '.encode())
        return zeni_machine_step

    def set_pos(self, azi, zeni):
        self.ser.write('a={azi} '.encode())
        self.ser.write('z=%d ' %zeni.encode())
        self.ser.write('GOSUB4 '.encode())

    def check_coords_inbounds(self, azi, zeni):
        # check if he wants helper method to check if they are inbounds
        # could be used for 

        return
        


    def convert_to_machine_steps(self, azi_world, zeni_world, azi_offset, zeni_offset, max_steps):
        # ask about negative components 
        azi = azi_world - azi_offset
        zeni = zeni_world - zeni_offset
        azi_machine_step = round((max_steps / 360) * azi)
        zeni_machine_step = round((max_steps / 360) * zeni)
        azi_machine_step = azi_machine_step % max_steps
        zeni_machine_step = zeni_machine_step % max_steps
        return azi_machine_step, zeni_machine_step

    def go_home(self):
        self.ser.write('GOSUB5 '.encode())


    def get_curr_coords(self):
       '''Gets target position of SmartMotor'''
       self.ser.write('RPA '.encode())
       process_az = self.ser.readline().decode()
       split_by_command_numbers = process_az.split(' ')
       split_by_hash = split_by_command_numbers[1].split('\r')
       az = (split_by_hash[0])
       ze = (split_by_hash[1])
       return az, ze

   

    def _openSerial(self):
        '''opens serial port and sets handle'''
        self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, \
            parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, \
            bytesize=serial.EIGHTBITS, timeout=1)
    
    def _closeSerial(self):
        self.ser.close()

    def stopMotor(self):
        self.ser.write('X ')
   
