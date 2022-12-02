#from distutils.command.config import config
#from multiprocessing.sharedctypes import Value
#from pickle import NONE
from asyncore import file_dispatcher
from inspect import CO_VARKEYWORDS
# from logging.config import _LoggerConfiguration

import sunau
import sys
import logging
# from os import sys, path
# sys.path.append('../config ')
# from config import config
# from main_scheduler import config
import serial
#import config.py
import keyboard
from time import sleep


# add stuff the homing
# fix the jog file
# make sure the coordinants are working correctly


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
    max_steps = None
    sun_location_azi = None
    sun_location_zeni = None
    moon_location_azi = None
    moon_location_zeni = None
    azi_offset = None
    zeni_offset = None
    azi_world = None
    zeni_world = None
    number_of_steps = None
    port_location = None

    def __init__(self, MaxSteps, SunLocationAzi, SunLocationZeni,  MoonLocationAzi, MoonLocationZeni, AziOffset, ZeniOffset, AziWorld, ZeniWorld, NumberOfSteps, Port):
        self.max_steps = MaxSteps
        self.sun_location_azi = SunLocationAzi
        self.sun_location_zeni = SunLocationZeni
        self.moon_location_azi = MoonLocationAzi
        self.sun_location_zeni = MoonLocationZeni
        self.azi_offset = AziOffset
        self.zeni_offset = ZeniOffset
        self.azi_world = AziWorld
        self.zeni_world = ZeniWorld
        self.number_of_steps = NumberOfSteps
        self.port_location = Port
        # max_steps = MaxSteps
        # self._setSmartMotorVariables()
        try:
            self._openSerial()
        except:
            print("Can't open serial port")
           #
        # finally:
        #     self._closeSerial()

    def set_pos_azi(self, azi_machine_step):
        strr = 'a=%d ' % azi_machine_step
        self.ser.write(strr.encode())
        self.ser.write('GOSUB4 '.encode())
        process_az = self.ser.readline().decode()

        # return azi

    def set_pos_zeni(self, zeni_machine_step):
        strr = 'z=%d ' % zeni_machine_step
        self.ser.write(strr.encode())
        self.ser.write('GOSUB4 '.encode())
        process_az = self.ser.readline().decode()

        return zeni_machine_step

    def set_pos(self, azi, zeni):
        self.ser.write(('a=%d ' % azi).encode())
        self.ser.write(('z=%d ' % zeni).encode())
        self.ser.write('GOSUB4 '.encode())
        process_az = self.ser.readline().decode()

    def set_pos_real(self, azi_world, zeni_world):
        azi, zeni = self.convert_to_machine_steps(azi_world, zeni_world)
        self.ser.write(('a=%d ' % azi).encode())
        self.ser.write(('z=%d ' % zeni).encode())
        self.ser.write(('GOSUB4 ').encode())
        process_az = self.ser.readline().decode()
        azi1, zeni1 = self.get_curr_coords()
        while (azi != zeni1 and zeni != azi1):
            print(azi, azi1, zeni, zeni1)
            azi1, zeni1 = self.get_curr_coords()
            sleep(2)
            print("Waiting")
        print("finshed mooving")

    def check_coords_inbounds(self, azi, zeni):
        # check if he wants helper method to check if they are inbounds
        # could be used for

        return


# do not use offset

# read config file_dispatche

# find the sun Coords

# point sky scanner ot that location

# call jog function (commnand line inputs using arrows )

# once sun is found give button push and set new coords of sun

# set differnce of where it thinks sun is versus where the motors are

# written to config file

    def convert_to_machine_steps(self, azi_world, zeni_world):
        # ask about negative components
        azi = -azi_world - self.azi_offset
        zeni = (-zeni_world) - self.zeni_offset + 180
        azi_machine_step = round((self.max_steps / 360) * azi)
        zeni_machine_step = round((self.max_steps / 360) * zeni)
        azi_machine_step = self.max_steps - (azi_machine_step % self.max_steps)
        zeni_machine_step = zeni_machine_step % self.max_steps
        return azi_machine_step, zeni_machine_step

    def convert_sun_to_machine_steps(self):
        # ask about negative components
        azi = -self.sun_location_azi - self.azi_offset
        zeni = (-self.sun_location_zeni) - self.zeni_offset + 180
        azi_machine_step = round((self.max_steps / 360) * azi)
        zeni_machine_step = round((self.max_steps / 360) * zeni)
        azi_machine_step = self.max_steps - (azi_machine_step % self.max_steps)
        zeni_machine_step = zeni_machine_step % self.max_steps
        return azi_machine_step, zeni_machine_step

    def jog(self):
        print("jogging please wait")
        machine_sun_azi, machine_sun_zeni = self.convert_sun_to_machine_steps()
        self.set_pos(machine_sun_azi, machine_sun_zeni)
        while (True):
            curr_az, curr_zen = self.get_curr_coords()
            print(curr_az, curr_zen, machine_sun_azi, machine_sun_zeni)
            if (curr_az == machine_sun_zeni and machine_sun_azi == curr_zen):
                break
        curr_az, curr_zen = self.get_curr_coords()
        print(
            "print finished moving to the sun's location - azi coord: {curr_az} zeni coord: {curr_zen}. Use the arrow keys to move the position of the Sky Scanner")
        while True:
            curr_az, curr_zen = self.get_curr_coords()
            if keyboard.is_pressed("q"):
                print("Exited Jog")
                break
            elif keyboard.is_pressed("left"):
                self.set_pos_azi(self, curr_az - 1)
                while (True):
                    curr_az1, curr_zen1 = self.get_curr_coords()
                    if (curr_az == curr_az1):
                        break
            elif keyboard.is_pressed("right"):
                self.set_pos_azi(self, curr_az + 1)
                while (True):
                    curr_az1, curr_zen1 = self.get_curr_coords()
                    if (curr_az == curr_az1):
                        break
            elif keyboard.is_pressed("down"):
                self.set_pos_azi(self, curr_zen - 1)
                while (True):
                    curr_az1, curr_zen1 = self.get_curr_coords()
                    if (curr_zen == curr_zen1):
                        break
            elif keyboard.is_pressed("up"):
                self.set_pos_azi(self, curr_zen + 1)
                while (True):
                    curr_az1, curr_zen1 = self.get_curr_coords()
                    if (curr_zen == curr_zen1):
                        break
        return

    def go_home(self):
        self.ser.write('GOSUB5 '.encode())
        sleep(15)
        logging.info('Homing Skyscanner')
        print("finshed mooving")

    def get_curr_coords(self):
        '''Gets target position of SmartMotor'''
        self.ser.write('RPA '.encode())
        process_az = self.ser.readline().decode()
        split_by_command_numbers = process_az.split(' ')
        split_by_hash = split_by_command_numbers[1].split('\r')
        print(split_by_hash)
        az = int(split_by_hash[0])
        ze = int(split_by_hash[1])
        return az, ze

    def _openSerial(self):
        '''opens serial port and sets handle'''
        self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600,
                                 parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                                 bytesize=serial.EIGHTBITS, timeout=1)

    def _closeSerial(self):
        self.ser.close()

    def stopMotor(self):
        self.ser.write('X ')
