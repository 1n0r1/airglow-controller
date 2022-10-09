from time import sleep
import andorsdk
import numpy as np
from PIL import Image

camera = andorsdk.Andorsdk()

camera.setParameters()
camera.startAcquisition()
while (camera.getStatus() != "DRV_IDLE"):
    sleep(1)
    
img = camera.getImage()
npimg = np.array(img)
npimg = npimg/np.max(npimg)*255
png = Image.fromarray(npimg)
png = png.convert('RGB')
png.save('test.png')

camera.shutDown()