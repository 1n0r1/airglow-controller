# Documenting what was done

Wine

Added R/W permission rule in udev/rules.d

KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0666", GROUP="plugdev"
udevadm control --reload-rules

A VM should work, last resort