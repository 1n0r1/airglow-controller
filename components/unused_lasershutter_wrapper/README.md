# Documenting what was done

Wine

Added R/W permission rule in udev/rules.d

KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0666", GROUP="plugdev"
udevadm control --reload-rules

A VM should work, last resort

# RPi I2C 
M1: red on left side and brown on right side
M2: yellow on left side and black on right side

stepper1.onestep() seven times to open
stepper1.release() to close
