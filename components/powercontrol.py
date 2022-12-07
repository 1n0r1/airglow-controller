import sys
import dlipower
import logging


class PowerControl:
    def __init__(self, hostname="192.168.1.100", userid="admin", password="ionosphere") -> None:
        self.switch=dlipower.PowerSwitch(hostname, userid, password)
        if not self.switch.verify():
            logging.error("Can't talk to the switch")

    def turnOn(self, port):
        self.switch.on(port)
        
    def turnOff(self, port):
        self.switch.off(port)
