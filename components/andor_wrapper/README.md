# Andor Camera

Example code on how to use the camera. Run the script from the main directory of this repo for import components.camera to work, else you might need to change
the import path.

```
  from components.camera import getCamera
  from PIL import Image as im
  
  camera = getCamera("Andor")
  
  # Initial setup
  camera.setReadMode() # Default is set mode=4 as image mode (other modes can be found in Andor's SDK documentation)
  camera.setImage() # Default is hbin=2, vbin=2, hstart=1, hend=1024, vstart=1, vend=1024
  camera.setShiftSpeed() # Default is indexH=2, indexV=2, preAmpGain=2, ttype=0 (refer to Andor's SDK documentation for other settings)
  
  # Set temperature
  print(camera.getTemperatureRange()) # Get supported temperature range
  desired_temp = -40
  camera.setTemperature(desired_temp)
  camera.turnOnCooler()
  
  # Wait until temperature stablize and print the temperature
  while (camera.getTemperature() > desired_temp + 5):
        print('CCD Temperature: ' + str(camera.getTemperature()))
        sleep(10)
  
  
  # Take picture
  exposure_time = 20 # in seconds I think
  camera.setShutter() # Default mode is open shutter. To take image while shutter is close do setShutter(mode=2), refer to Andor SDK's doc for more
  camera.setExposureTime(exposure_time)
  camera.startAcquisition()
  sleep(exposure_time)
  while (camera.getStatus() == "DRV_ACQUIRING"):
      sleep(2)
  nparr = camera.getImage() # return image as numpy array
  image = im.fromarray(nparr) # convert numpy array to image
  image.save('./test.png') # save image to file
  
  
  # Warm the camera back up slowly so that the CCD is not damaged
  camera.turnOffCooler()
  while (camera.getTemperature() < -20):
      print('CCD Temperature: ' + str(camera.getTemperature()))
      sleep(10)
      
  # Shutdown/disconnect camera afterward
  camera.shutDown()
```
