# Initial setup for Odyssey

Install Ubuntu 22.04 with erase disk and wipe out old operating system (Windows)

## Setup RDP

`sudo apt install xrdp`
check status:
`sudo systemctl status xrdp`
If it is not running you might need to turn off Ubuntu's native RDP (which is less convenient than xrdp)
Log out and test RDP

## Setup SSH
`sudo apt install openssh-server`
check status:
`sudo systemctl status ssh`


# Installing Andor SDK

Download Andor SDK2.104.30064.0

Extract then `sudo ./install_andor`


Andor SDK also require libusb:

`sudo apt-get install g++`

`sudo apt-get install libusb-dev`

Test sdk by `make` an example and try running it

After successful installation of Andor SDK, `libandor.so` should appear in `/usr/local/lib/`. This is the shared library that we can use to call the SDK functions in Python with ctypes.

## Cython for SDK

cd into `components/andorsdk_wrapper/` and `python3 setup.py build_ext -i` to build the python module

Now you can import to python `components/andorsdk_wrapper/andorsdk`
