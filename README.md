# Initial setup for Odyssey

Install Ubuntu 22.04 with erase disk and wipe out old operating system (Windows)

Also set Restore on AC/Power Loss to Power On in the BIOS
## Setup RDP

`sudo apt install xrdp`

check status:

`sudo systemctl status xrdp`

If it is not running you might need to turn off Ubuntu's native RDP (which is less convenient than xrdp).
Log out and test RDP

## Setup SSH

`sudo apt install openssh-server`

check status:

`sudo systemctl status ssh`


# Setup for Raspberry Pi
Install Raspberry Pi OS 32-bit

Switch from DHCPCD to NetworkManager

Enable SSH in Configuration

`sudo apt install xrdp`

`sudo adduser airglowrdp`

RDP to RPi need to be from a different user `airglowrdp` and not the default one `airglow`

# Installing Andor SDK

Download Andor SDK2.104.30064.0

Extract `tar -xvf andor-` then `sudo ./install_andor`


Andor SDK also require libusb:

`sudo apt-get install g++`

`sudo apt-get install libusb-dev`

Test sdk by `make` an example and try running it

After successful installation of Andor SDK, `libandor.so` should appear in `/usr/local/lib/`. This is the shared library that we can use to call the SDK functions in Python with ctypes.

# Python
`sudo apt-get update`

`sudo apt-get install python3.6`

`sudo apt-get install python3-pip`

Clone this repo into home dir `~/airglow/airglow-controller`

`pip3 install -r requirements.txt`

## Cython for SDK

cd into `components/andor_wrapper/andorsdk_wrapper` and `python3 setup.py build_ext -i` to build the python module

Now you can import to python `components/andorsdk_wrapper/andorsdk`
