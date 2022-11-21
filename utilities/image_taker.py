from time import sleep
import h5py
from datetime import datetime

class Image_Helper:
    counter = None
    folderName = None
    camera = None
    def __init__(self, folderName, camera) -> None:
        self.counter = {
            "image": 0,
            "dark": 0,
            "laser": 0,
            "bias": 0
        }
        self.folderName = folderName
        self.camera = camera

    def save_image(self, type, imgData, exp, az, ze):
        data_files = h5py.File(self.folderName + '/' +
                               type + '_' + datetime.utcnow().strftime('%Y%m%d%H%M%D_') + str(self.counter[type]) + '.hdf5', 'w')
        # Log
        f = data_files.create_dataset("image", data=imgData)
        f.attrs['ExposureTime'] = exp
        f.attrs['azAngle'] = az
        f.attrs['zeAngle'] = ze
        f.attrs['LocalTime'] = str(datetime.now())
        f.attrs['CCDTemperature'] = self.camera.getTemperature()
        f.attrs['OutsideTemperature'] = 20
        f.attrs['Pressure'] = 20

        data_files.close()
        self.counter[type] += 1

    def take_initial_image(self, exposure, az, ze):
        # closes shutter
        self.camera.setShutter(mode=2)
        self.camera.setExposureTime(exposure)
        self.camera.startAcquisition()
        while (self.camera.getStatus() == "DRV_ACQUIRING"):
            sleep(2)
        nparr = self.camera.getImage()
        self.save_image("dark", nparr, exposure, az, ze)

        return nparr

    def take_normal_image(self, exposure, az, ze):
        # keeps shutter open by default
        self.camera.setShutter()
        self.camera.setExposureTime(exposure)
        self.camera.startAcquisition()
        while (self.camera.getStatus() == "DRV_ACQUIRING"):
            sleep(2)
        nparr = self.camera.getImage()
        self.save_image("image", nparr, exposure, az, ze)
        return nparr

    # function for laser image

    def take_laser_image(self, exposure, skyscanner, lasershutter, az, zen):
        skyscanner.set_pos_real(az, zen)
        # move filterwheel
        lasershutter.open_shutter()
        self.camera.setShutter()
        self.camera.setExposureTime(exposure)
        self.camera.startAcquisition()
        while (self.camera.getStatus() == "DRV_ACQUIRING"):
            sleep(2)
        nparr = self.camera.getImage()
        lasershutter.close_shutter()
        self.save_image("laser", nparr, exposure, az, zen)
        return nparr
