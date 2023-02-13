import sys
import os
import logging

# This import only works if camera.py is imported from outside components (see main_scheduler.py for import)
# Will not work if import inside components
from .andor_wrapper.andor_camera import AndorCamera


def getCamera(name):
    if (name == "Andor"):
        return AndorCamera()
    return None
