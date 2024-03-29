# Tested on
Ubuntu 22.04

Python 3.10.6

Make a file `config.py` following `config.py.example` to setup configuration for different sites.
Make a file `schedule.py` following `schedule.py.example` to setup configuration for different sites.

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

## Add user to dialout group

`sudo adduser airglow dialout`

## Udev rule for USB Shutter

`sudo apt install libhidapi-hidraw0`

`sudo nano /etc/udev/rules.d/99-laser-shutter.rules`

Then write the following into the file `KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0666"`

Then reboot

`ls -l /dev/` to verify the permission for hidraw0, it should be `crw-rw-rw-`


# Setup for Raspberry Pi
Install Raspberry Pi OS 32-bit

Switch from DHCPCD to NetworkManager

Enable SSH and Serial Port in Configuration

`sudo apt install xrdp`

`sudo adduser airglowrdp`

RDP to RPi need to be from a different user `airglowrdp` and not the default one `airglow`

Delete the command that use serial0 on RPi:

`sudo nano /boot/cmdline.txt`

and ONLY delete `console=serial0,115200`, keep the rest of the line unchanged

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

Install Python 3.10.6

`sudo apt-get install python3-pip`

Clone this repo into home dir `~/airglow/airglow-controller`

`pip3 install -r requirements.txt`

## Cython for SDK

`sudo apt-get install build-essential python3-dev`

cd into `components/andor_wrapper/andorsdk_wrapper` and `python3 setup.py build_ext -i` to build the python module

Now you can import to python `components/andorsdk_wrapper/andorsdk`

## Laser Shutter

Use lsusb to view the vendorId and productId of the connected laser shutter, vendorId:productId, for example 0461:0030. Write in config file as 0x0461 and 0x0030.

Remember to set the udev rule for laser shutter (written above)

## Connection test

`python3 connection_test.py` to test all the components

## Set crontab
`crontab -l`

## Setup static USB port
Should update for actual text direction. Meanwhile here is a picture.
![image](https://github.com/1n0r1/airglow-controller/assets/80285371/4cf66383-d5b0-44f2-8db4-d39c832494c4)


## Gmail setup (optional)

Unneccessarily hard to setup for some reason. Could look into replacing it with other less complex alternative

If you want to use a different gmail account or don't have a working `gmailcredential.json` file, follows https://www.thepythoncode.com/article/use-gmail-api-in-python to Enable Gmail API. Then download `gmailcredential.json` file and specify the path in config['gmailCred'].

Run connection_test.py to check if gmail works, go to the verification link if neccessary. 

airglowuaotest@gmail.com

airglow123;
