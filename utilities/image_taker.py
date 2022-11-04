
def take_initial_image(camera, exposure):
    # closes shutter
    camera.setShutter(mode=2)
    camera.setExposureTime(exposure)
    camera.startAcquisition()
    while (camera.getStatus == "DRV_ACQUIRING"):
        sleep(2)
    nparr = camera.getImage()
    return nparr

def take_normal_image(camera, exposure):
    # keeps shutter open by default
    camera.setShutter()
    camera.setExposureTime(exposure)
    camera.startAcquisition()
    while (camera.getStatus == "DRV_ACQUIRING"):
        sleep(2)
    nparr = camera.getImage()
    return nparr

# function for laser image





    