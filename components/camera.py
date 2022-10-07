from andorsdk_wrapper import andorsdk
from andorsdk_wrapper import errorcodestable

camera = andorsdk.Andorsdk()
temperature = camera.getTemperature()
print(temperature)
camera.setTemperature(-20)

