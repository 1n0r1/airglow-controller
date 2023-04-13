import sys
import dlipower
import logging


class PowerControl:
    def __init__(self, hostname="192.168.1.100", userid="admin", password="ionosphere") -> None:
        self.switch = dlipower.PowerSwitch(hostname=hostname, userid=userid, password=password, timeout=60, retries=5)
        if not self.switch.verify():
            logging.error("Can't talk to the switch")
        logging.info("Connected to power switch")

    def turnOn(self, port):
        res = self.switch.on(port)
        logging.info("Powered on port " + str(port) + " response: " + str(res))
        
    def turnOff(self, port):
        res = self.switch.off(port)
        logging.info("Powered off port " + str(port) + " response: " + str(res))
        
    def cycle(self, port):
        res = self.switch.cycle(port)
        logging.info("Cycled port " + str(port) + " response: "+ str(res))
