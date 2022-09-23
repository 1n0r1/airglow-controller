from andorsdk_wrapper import andorsdk

camera = andorsdk.Andorsdk()
temperature = camera.getTemperature()
print(temperature)
