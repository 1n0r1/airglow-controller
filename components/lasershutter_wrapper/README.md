# Documenting what was done

Wine

Added R/W permission rule in udev/rules.d

KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0664", GROUP="plugdev"

A VM should work, last resort
