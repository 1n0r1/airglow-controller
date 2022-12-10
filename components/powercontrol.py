import sys
import dlipower
import logging


class PowerControl:
    def __init__(self, hostname="192.168.1.100", userid="admin", password="ionosphere") -> None:
        self.switch=dlipower.PowerSwitch(hostname=hostname, userid=userid, password=password)
        if not self.switch.verify():
            logging.error("Can't talk to the switch")
        logging.info("Connected to power switch")

    def turnOn(self, port):
        self.switch.on(port)
        logging.info("Powered on port " + str(port))
        
    def turnOff(self, port):
        self.switch.off(port)
        logging.info("Powered off port " + str(port))
