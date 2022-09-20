# Getting started
Ubuntu 22.04

## Installing Andor SDK

Download Andor SDK2.104.30064.0

Extract then `sudo ./install_andor`


Andor SDK also require libusb:

`sudo apt-get install g++`

`sudo apt-get install libusb-dev`

Test sdk by `make` an example and try running it

After successful installation of Andor SDK, `libandor.so` should appear in `/usr/local/lib/`. This is the shared library that we can use to call the SDK functions in Python with ctypes.
