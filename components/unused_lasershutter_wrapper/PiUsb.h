// PiUsb.h   Function definitions
// Version 2.3  2021-06-12

#ifndef PIUSB_H
#define PIUSB_H

/*
	@file PiUsb.h
	@brief Functions in the PiUsb API.
*/

/**
	@defgroup Handles Handles
	Typedefs and macros used to define device handles.
	@{
*/

///	<summary>
///	Typedef for a device handle.
///	</summary>
/// <remarks>
///	@sa @ref DeviceHandle
///	</remarks>
typedef void * PIHANDLE;

///	<summary>
///	Constant for an invalid device handle.
///	</summary>
#define INVALID_PIHANDLE ((PIHANDLE)0)

/** @} */ // end of Handles group

/** @defgroup ErrorNumbers Error Numbers
	Success or error return values.
	Most functions in the PiUsb API return an integer Error Number which indicates
    whether the function succeeded of failed, and the cause of any failure.
    @sa @ref ErrorHandling
	@{
*/

///	<summary>
///	No error.
///	</summary>
///	<remarks>
///	The operation was successful.
/// @sa @ref ErrorHandling
///	</remarks>
#define PI_NO_ERROR 0

///	<summary>
///	Device not found.
///	</summary>
///	<remarks>
///	The specified device could not be found or has been disconnected.
/// @sa @ref ErrorHandling
///	</remarks>
#define PI_DEVICE_NOT_FOUND 1

///	<summary>
///	Device handle does not exist.
///	</summary>
///	<remarks>
///	The device handle does not exist or is null.
/// @sa @ref ErrorHandling
///	</remarks>
#define PI_OBJECT_NOT_FOUND 2

///	<summary>
///	Cannot create a device handle for the specified device.
///	</summary>
///	<remarks>
///	The system was unable to allocate memory for the requested device.
/// @sa @ref ErrorHandling
///	</remarks>
#define PI_CANNOT_CREATE_OBJECT 3

///	<summary>
///	Invalid device handle.
///	</summary>
///	<remarks>
/// The device handle specifies a device that cannot be used with this function.
/// @sa @ref ErrorHandling
///	</remarks>
#define PI_INVALID_DEVICE_HANDLE 4

///	<summary>
///	Timeout while attempting to read from the device.
///	</summary>
///	<remarks>
///	The system timed out while attempting to read data from the device.
/// This usually means that the device has been disconnected.
/// @sa @ref ErrorHandling
///	</remarks>
#define PI_READ_TIMEOUT 5

///	<summary>
///	The system abandoned the read operation.
///	</summary>
///	<remarks>
///	The system thread that is reading from the device has exited or been killed.
/// Disconnect from the device and attempt to reconnect to it.
/// @sa @ref ErrorHandling
///	</remarks>
#define PI_READ_THREAD_ABANDONED 6

///	<summary>
///	An attempt to read from the device failed.
///	</summary>
///	<remarks>
///	The system reported a failure when attempting to read from the device.
/// Disconnect from the device and attempt to reconnect to it.
/// @sa @ref ErrorHandling
///	</remarks>
#define PI_READ_FAILED 7

///	<summary>
///	An invalid parameter value was passed to a function.
///	</summary>
///	<remarks>
/// @sa @ref ErrorHandling
///	</remarks>
#define PI_INVALID_PARAMETER 8

///	<summary>
///	An attempt to write to the device failed.
///	</summary>
///	<remarks>
///	The system reported a failure when attempting to write to the device.
/// Disconnect from the device and attempt to reconnect to it.
/// @sa @ref ErrorHandling
///	</remarks>
#define PI_WRITE_FAILED 9

/** @} */ // end of ErrorNumbers group


/** @defgroup ProductID Product IDs
	Values returned by ::piFindDevices() to identify the type of device.
    @sa @ref ::piFindDevices()
    @sa @ref Discovery
	@{
*/

///	<summary>
///	All Picard Industries devices.
///	</summary>
#define PRODUCT_ID_ALL    0x0000

///	<summary>
///	Relay device.
///	</summary>
///	<remarks>
///	The Relay and Valve products share the same Product ID.
///	</remarks>
#define PRODUCT_ID_RELAY    0x0010

///	<summary>
///	Valve device.
///	</summary>
///	<remarks>
///	The Relay and Valve products share the same Product ID.
///	</remarks>
#define PRODUCT_ID_VALVE    0x0010

///	<summary>
///	Laser device.
///	</summary>
///	<remarks>
///	</remarks>
#define PRODUCT_ID_LASER    0x0011

///	<summary>
///	Motor device.
///	</summary>
///	<remarks>
/// The motor device applies to the MO, MO-2, Slide, Slide-2, and Labjack devices.
///	</remarks>
#define PRODUCT_ID_MOTOR    0x0020

///	<summary>
///	Twister device.
///	</summary>
///	<remarks>
/// The twister device applies to the Twister, Twister-2, Twister-3, and Super-Twister devices.
///	</remarks>
#define PRODUCT_ID_TWISTER  0x0021

///	<summary>
///	Shutter device.
///	</summary>
///	<remarks>
///	</remarks>
#define PRODUCT_ID_SHUTTER  0x0030

///	<summary>
///	Flipper device.
///	</summary>
///	<remarks>
///	</remarks>
#define PRODUCT_ID_FLIPPER  0x0040

///	<summary>
///	Filter Wheel device.
///	</summary>
///	<remarks>
///	The Filter Wheel, Gradient Wheel, and Rotator products share the same Product ID.
///	</remarks>
#define PRODUCT_ID_FILTER   0x0050

///	<summary>
///	Gradient Wheel device.
///	</summary>
///	<remarks>
///	The Filter Wheel, Gradient Wheel, and Rotator products share the same Product ID.
///	</remarks>
#define PRODUCT_ID_GRADIENT 0x0050

///	<summary>
///	Rotator device.
///	</summary>
///	<remarks>
///	The Filter Wheel, Gradient Wheel, and Rotator products share the same Product ID.
///	</remarks>
#define PRODUCT_ID_ROTATOR  0x0050

/** @} */ // end of ProductID group


// If BOOL is not defined, define it.
#ifndef BOOL
typedef int BOOL;
#endif

// Use the C linkage convention.
#ifdef __cplusplus
extern "C" {
#endif

/**
	@defgroup FilterFunctions Filter Wheel Functions
	Functions to control USB Filter Wheel devices
    You can also connect to and control Filter Wheel devices using the
    @ref GradientFunctions and @ref RotatorFunctions.
	@{
*/

/// <summary>
///	Search for connected USB Filter Wheel devices
///	</summary>
///	<param name="DeviceCount"><c>[out]</c> The number of devices found. This is the number
/// of values returned in @p SerialNumberArray.</param>
///	<param name="SerialNumberArray"><c>[in/out]</c> An array of
/// device serial numbers. It must be pre-allocated to be @p ArraySize
/// in length. It will be returned with @p DeviceCount values set.
/// </param>
///	<param name="ArraySize"><c>[in]</c> The size of the
/// @p SerialNumberArray arrays as passed into this function.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// Searches for connected Picard Industries Filter devices, and returns an array of
/// Serial Numbers.
///
/// Note that Filter Wheel, Gradient Wheel, and Rotator devices share the same ProductID, and
/// are therefore not distinguishable. This function will return all Filter Wheel,
/// Gradient Wheel, and Rotator devices.
/// @sa @ref Discovery
/// </remarks>
int __stdcall piFindFilters(int* DeviceCount, int* SerialNumberArray, int ArraySize);

/// <summary>
///	Connect to a USB Filter Wheel.
///	</summary>
///	<param name="ErrorNumber"><c>[out]</c> An @ref ErrorNumbers "error number".</param>
///	<param name="SerialNum"><c>[in]</c> The device serial number.</param>
///	<returns>The device handle for the new device. If the device is not found or an
/// error occurs, NULL is returned.</returns>
/// <remarks>
/// @sa ::piDisconnectFilter()
/// </remarks>
PIHANDLE __stdcall piConnectFilter(int * ErrorNumber, int SerialNum);

/// <summary>
///	Disconnect from a USB Filter Wheel.
///	</summary>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// @sa ::piConnectFilter()
/// </remarks>
void __stdcall piDisconnectFilter(PIHANDLE handle);

/// <summary>
///	Get the filter wheel position.
///	</summary>
///	<param name="Position"><c>[out]</c> The current position of the filter wheel.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// For a standard filter wheel, the reported position will be between 1 and 6.
/// Custom devices can have up to 16 positions.
/// </para>
/// <para>
/// The @p Position will be set to 0 if the filter wheel is between positions.
/// While moving the position will be reported as 0 most of the time, but
/// will report a positive value as it passes through each position.
/// </para>
/// @sa ::piSetFilterPosition()
/// </remarks>
int __stdcall piGetFilterPosition(int * Position, PIHANDLE handle);

/// <summary>
///	Initiate a move to a new filter wheel position.
///	</summary>
///	<param name="Destination"><c>[in]</c> The destination position of the filter wheel.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// For a standard filter wheel, the destination position should be between 1 and 6.
/// Custom devices can have up to 16 positions.
/// </para>
/// <para>
/// Setting the position to 0 will cause the filter wheel to stop immediately.
/// </para>
/// @sa ::piGetFilterPosition()
/// </remarks>
int __stdcall piSetFilterPosition(int Destination, PIHANDLE handle);

/** @} */ // end of FilterFunctions group


/**
	@defgroup GradientFunctions Gradient Wheel Functions
	Functions to control USB Gradient Wheel devices
    You can also connect to and control Gradient Wheel devices using the
    @ref RotatorFunctions.
	@{
*/

/// <summary>
///	Search for connected USB Gradient Wheel devices
///	</summary>
///	<param name="DeviceCount"><c>[out]</c> The number of devices found. This is the number
/// of values returned in @p SerialNumberArray.</param>
///	<param name="SerialNumberArray"><c>[in/out]</c> An array of
/// device serial numbers. It must be pre-allocated to be @p ArraySize
/// in length. It will be returned with @p DeviceCount values set.
/// </param>
///	<param name="ArraySize"><c>[in]</c> The size of the
/// @p SerialNumberArray arrays as passed into this function.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// Searches for connected Picard Industries Gradient Wheel devices, and returns an array of
/// Serial Numbers.
///
/// Note that Filter Wheel, Gradient Wheel, and Rotator devices share the same ProductID, and
/// are therefore not distinguishable. This function will return all Filter Wheel,
/// Gradient Wheel, and Rotator devices.
/// @sa @ref Discovery
/// </remarks>
int __stdcall piFindGWheels(int* DeviceCount, int* SerialNumberArray, int ArraySize);

/// <summary>
///	Connect to a USB Gradient Wheel.
///	</summary>
///	<param name="ErrorNumber"><c>[out]</c> An @ref ErrorNumbers "error number".</param>
///	<param name="SerialNum"><c>[in]</c> The device serial number.</param>
///	<returns>The device handle for the new device. If the device is not found or an
/// error occurs, NULL is returned.</returns>
/// <remarks>
/// @sa ::piDisconnectGWheel()
/// </remarks>
PIHANDLE __stdcall piConnectGWheel(int * ErrorNumber, int SerialNum);

/// <summary>
///	Disconnect from a USB Gradient Wheel.
///	</summary>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// @sa ::piConnectGWheel()
/// </remarks>
void __stdcall piDisconnectGWheel(PIHANDLE handle);

/// <summary>
///	Get the gradient wheel position.
///	</summary>
///	<param name="Position"><c>[out]</c> The current position of the gradient wheel.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// The reported position will be between 1 and 1023.
/// </para>
/// @sa ::piSetGWheelPosition()
/// </remarks>
int __stdcall piGetGWheelPosition(int * Position, PIHANDLE handle);

/// <summary>
///	Initiate a move to a new gradient wheel position.
///	</summary>
///	<param name="Destination"><c>[in]</c> The destination position of the gradient wheel.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// The destination position should be between 1 and 1023.
/// </para>
/// <para>
/// Setting the position to 0 will cause the gradient wheel to stop immediately.
/// </para>
/// @sa ::piGetGWheelPosition()
/// </remarks>
int __stdcall piSetGWheelPosition(int Destination, PIHANDLE handle);

/** @} */ // end of GradientFunctions group

/**
	@defgroup FlipperFunctions Flipper Functions
	Functions to control USB Flipper devices
	@{
*/

/** @defgroup FlipperConstants Flipper Constants
	State of the Flipper
	@{
*/

///	<summary>
///	Flipper is retracted (closed).
///	</summary>
#define PI_FLIPPER_RETRACTED 0

///	<summary>
///	Flipper is extended (open).
///	</summary>
#define PI_FLIPPER_EXTENDED 1

/** @} */ // end of FlipperConstants group

/// <summary>
///	Search for connected USB Flipper devices
///	</summary>
///	<param name="DeviceCount"><c>[out]</c> The number of devices found. This is the number
/// of values returned in @p SerialNumberArray.</param>
///	<param name="SerialNumberArray"><c>[in/out]</c> An array of
/// device serial numbers. It must be pre-allocated to be @p ArraySize
/// in length. It will be returned with @p DeviceCount values set.
/// </param>
///	<param name="ArraySize"><c>[in]</c> The size of the
/// @p SerialNumberArray arrays as passed into this function.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// Searches for connected Picard Industries Flipper devices, and returns an array of
/// Serial Numbers.
/// @sa @ref Discovery
/// </remarks>
int __stdcall piFindFlippers(int* DeviceCount, int* SerialNumberArray, int ArraySize);

/// <summary>
///	Connect to a USB Flipper.
///	</summary>
///	<param name="ErrorNumber"><c>[out]</c> An @ref ErrorNumbers "error number".</param>
///	<param name="SerialNum"><c>[in]</c> The device serial number.</param>
///	<returns>The device handle for the new device. If the device is not found or an
/// error occurs, NULL is returned.</returns>
/// <remarks>
/// @sa ::piDisconnectFlipper()
/// </remarks>
PIHANDLE __stdcall piConnectFlipper(int * ErrorNumber, int SerialNum);

/// <summary>
///	Disconnect from a USB Flipper.
///	</summary>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// @sa ::piConnectFlipper()
/// </remarks>
void __stdcall piDisconnectFlipper(PIHANDLE handle);

/// <summary>
///	Get the flipper state.
///	</summary>
///	<param name="FlipperState"><c>[out]</c> The current state of the flipper.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// @p FlipperState will be returned as one of:
/// </para>
/// <list type="bullet">
///   <item>#PI_FLIPPER_RETRACTED</item>
///   <item>#PI_FLIPPER_EXTENDED</item>
/// </list>
/// <para>
/// Immediately after powering up the flipper, the flipper will be retracted.
/// </para>
/// <para>
/// The flipper device contains a sensor which reports the actual state of the flipper.
/// If the flipper is physically blocked from moving, or you manually move the flipper,
/// piGetFlipperState will return the actual state and not state commanded with
/// ::piSetFlipperState(). This is in contrast to a @ref ShutterFunctions "Shutter device"
/// which has no sensor and ::piGetShutterState will return the commanded state.
/// </para>
/// @sa ::piSetFlipperState()
/// </remarks>
int __stdcall piGetFlipperState(int *FlipperState, PIHANDLE handle);

/// <summary>
///	Set the flipper state.
///	</summary>
///	<param name="FlipperState"><c>[in]</c> The state of the flipper to set.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// The flipper will be set to the specified state.
/// Valid values are:
/// </para>
/// <list type="bullet">
///   <item>#PI_FLIPPER_RETRACTED</item>
///   <item>#PI_FLIPPER_EXTENDED</item>
/// </list>
/// <para>
/// The flipper device contains a sensor which reports the actual state of the flipper.
/// If the flipper is physically blocked from moving, or you manually move the flipper,
/// piGetFlipperState will return the actual state and not state commanded with
/// ::piSetFlipperState(). You may want to keep track of the most recently commanded
/// state in order to toggle to the opposite state even if the flipper was physically
/// blocked.
/// </para>
/// @sa ::piGetFlipperState()
/// </remarks>
int __stdcall piSetFlipperState(int FlipperState, PIHANDLE handle);

/** @} */ // end of FlipperFunctions group

/**
	@defgroup LaserFunctions Laser Functions
	Functions to control USB Laser devices
	@{
*/

/** @defgroup LaserConstants Laser Constants
	State of the Laser
	@{
*/

///	<summary>
///	Laser is off.
///	</summary>
#define PI_LASER_OFF 0

///	<summary>
///	Laser is on.
///	</summary>
#define PI_LASER_ON 1

/** @} */ // end of LaserConstants group

/// <summary>
///	Search for connected USB Laser devices
///	</summary>
///	<param name="DeviceCount"><c>[out]</c> The number of devices found. This is the number
/// of values returned in @p SerialNumberArray.</param>
///	<param name="SerialNumberArray"><c>[in/out]</c> An array of
/// device serial numbers. It must be pre-allocated to be @p ArraySize
/// in length. It will be returned with @p DeviceCount values set.
/// </param>
///	<param name="ArraySize"><c>[in]</c> The size of the
/// @p SerialNumberArray arrays as passed into this function.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// Searches for connected Picard Industries Laser devices, and returns an array of
/// Serial Numbers.
/// @sa @ref Discovery
/// </remarks>
int __stdcall piFindLasers(int* DeviceCount, int* SerialNumberArray, int ArraySize);

/// <summary>
///	Connect to a USB Laser.
///	</summary>
///	<param name="ErrorNumber"><c>[out]</c> An @ref ErrorNumbers "error number".</param>
///	<param name="SerialNum"><c>[in]</c> The device serial number.</param>
///	<returns>The device handle for the new device. If the device is not found or an
/// error occurs, NULL is returned.</returns>
/// <remarks>
/// @sa ::piDisconnectLaser()
/// </remarks>
PIHANDLE __stdcall piConnectLaser(int * ErrorNumber, int SerialNum);

/// <summary>
///	Disconnect from a USB Laser.
///	</summary>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// @sa ::piConnectLaser()
/// </remarks>
void __stdcall piDisconnectLaser(PIHANDLE handle);

/// <summary>
///	Get the laser state.
///	</summary>
///	<param name="LaserState"><c>[out]</c> The current state of the laser.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// @p LaserState will be returned as one of:
/// </para>
/// <list type="bullet">
///   <item>#PI_LASER_OFF</item>
///   <item>#PI_LASER_ON</item>
/// </list>
/// <para>
/// Immediately after powering up the laser, the laser will be off.
/// </para>
/// @sa ::piSetLaserState()
/// </remarks>
int __stdcall piGetLaserState(int * LaserState, PIHANDLE handle);

/// <summary>
///	Set the laser state.
///	</summary>
///	<param name="LaserState"><c>[in]</c> The state of the laser to set.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// The laser will be set to the specified state.
/// Valid values are:
/// </para>
/// <list type="bullet">
///   <item>#PI_LASER_OFF</item>
///   <item>#PI_LASER_ON</item>
/// </list>
/// @sa ::piGetLaserState()
/// </remarks>
int __stdcall piSetLaserState(int LaserState, PIHANDLE handle);

/** @} */ // end of LaserFunctions group

/**
	@defgroup MotorFunctions Motor Functions
	Functions to control USB Motor devices

    @anchor MotorPosition
    @par USB Motor Position

    The USB Motor uses a stepper motor to rotate a lead screw.
    You command the motor to move to a new position with the ::piRunMotorToPosition()
    function, specifying the destination position in steps (or counts). There are
    200 steps for each revolution of the lead screw. How far the device attached to the
    lead screw advances with each step depends on the pitch of the lead screw.
    You can specify any position between 1 and 2 31 -1, but the physical upper limit
    depends on the device. Standard devices and their limits are:

    Device      | Limit (steps)
    ----------- | ------------:
    USB Motor 1 |   1,900
    USB Motor 2 |   5,600
    USB Pusher  |  50,000
    USB LabJack | 200,000

    You can read the current position at any time (while moving or not) with the
    :: piGetMotorPosition() and ::piGetMotorStatus() functions. The position will
    be set to zero when you home the device with ::piHomeMotor() function.

    @anchor MotorVelocity
    @par USB Motor Velocity

    The :piRunMotorToPosition() and piHomeMotor() functions require you to specify
    the velocity of the motion. The velocity is a number between 1 and 12, where 1
    is the slowest speed and 12 is the highest speed.

    We recommend that you limit your velocity to be 10 or less. These velocities
    should work well with most devices you connect to the Motor. If your load is
    small and light, you may be able to use faster velocities (11 and 12). If
    you attempt to move too large a load at too high a speed, the motor may stall,
    or may miss steps and not move the full distance.

    The following table shows the velocity settings and the approximate speed
    they correspond to:

    Velocity  | Steps/sec
    :-------: | :--------:
    1         | 133
    2         | 143
    3         | 154
    4         | 167
    5         | 182
    6         | 200
    7         | 222
    8         | 250
    9         | 286
    10        | 333
    11        | 400
    12        | 500

	@{
*/

/// <summary>
///	Search for connected USB Motor devices
///	</summary>
///	<param name="DeviceCount"><c>[out]</c> The number of devices found. This is the number
/// of values returned in @p SerialNumberArray.</param>
///	<param name="SerialNumberArray"><c>[in/out]</c> An array of
/// device serial numbers. It must be pre-allocated to be @p ArraySize
/// in length. It will be returned with @p DeviceCount values set.
/// </param>
///	<param name="ArraySize"><c>[in]</c> The size of the
/// @p SerialNumberArray arrays as passed into this function.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// Searches for connected Picard Industries Motor devices, and returns an array of
/// Serial Numbers.
/// @sa @ref Discovery
/// </remarks>
int __stdcall piFindMotors(int* DeviceCount, int* SerialNumberArray, int ArraySize);

/// <summary>
///	Connect to a USB Motor.
///	</summary>
///	<param name="ErrorNumber"><c>[out]</c> An @ref ErrorNumbers "error number".</param>
///	<param name="SerialNum"><c>[in]</c> The device serial number.</param>
///	<returns>The device handle for the new device. If the device is not found or an
/// error occurs, NULL is returned.</returns>
/// <remarks>
/// @sa ::piDisconnectMotor()
/// </remarks>
PIHANDLE __stdcall piConnectMotor(int * ErrorNumber, int SerialNum);

/// <summary>
///	Disconnect from a USB Motor.
///	</summary>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// @sa ::piConnectMotor()
/// </remarks>
void __stdcall piDisconnectMotor(PIHANDLE handle);

/// <summary>
///	Get the state of the home switch.
///	</summary>
///	<param name="AtHome"><c>[out]</c> The state of the home switch.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// @p AtHome will be @p TRUE when at the home position, and @p FALSE otherwise.
/// @sa ::piHomeMotor()
/// </remarks>
int __stdcall piGetMotorHomeStatus(BOOL * AtHome, PIHANDLE handle);

/// <summary>
///	Get a value indicating whether the motor is moving.
///	</summary>
///	<param name="Moving"><c>[out]</c> @p TRUE if the motor is moving, @p FALSE otherwise.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// @sa ::piRunMotorToPosition()
/// </remarks>
int __stdcall piGetMotorMovingStatus(BOOL * Moving, PIHANDLE handle);

/// <summary>
///	Get the position of the motor.
///	</summary>
///	<param name="Position"><c>[out]</c> The current position of the motor.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// The @p Position is a value between 1 and 2<sup>31</sup>-1, but the
/// physical upper limit depends on the device. See @ref MotorPosition "Motor Position".
/// </para>
/// @sa @ref MotorPosition "Motor Position"
/// @sa ::piRunMotorToPosition()
/// </remarks>
int __stdcall piGetMotorPosition(int * Position, PIHANDLE handle);

/// <summary>
///	Get the position and status of the motor.
///	</summary>
///	<param name="Position"><c>[out]</c> The current position of the motor.</param>
///	<param name="AtHome"><c>[out]</c> The state of the home switch.</param>
///	<param name="Moving"><c>[out]</c> @p TRUE if the motor is moving, @p FALSE otherwise.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// This method gets the current motor position and status in a single function call.
/// It returns the value of the ::piGetMotorPosition(), ::piGetMotorMovingStatus(), and
/// ::piGetMotorHomeStatus() functions.
/// </para>
/// <para>
/// It is more efficient to call this function rather than calling 3 separate functions.
/// Using this method reduces I/O traffic to the device and can improve the responsiveness
/// of your application.
/// </para>
/// <para>
/// The @p Position is a value between 1 and 2<sup>31</sup>-1, but the
/// physical upper limit depends on the device. See @ref MotorPosition "Motor Position".
/// </para>
/// @sa @ref MotorPosition "Motor Position"
/// @sa ::piRunMotorToPosition()
/// </remarks>
int __stdcall piGetMotorStatus(int * Position, BOOL* Moving, BOOL* AtHome, PIHANDLE handle);

/// <summary>
///	Get the velocity of the motor.
///	</summary>
///	<param name="Velocity"><c>[out]</c> The velocity of the motor.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// @sa @ref MotorVelocity "Motor Velocity"
/// @sa ::piRunMotorToPosition()
/// @sa ::piHomeMotor()
/// </remarks>
int __stdcall piGetMotorVelocity(int * Velocity, PIHANDLE handle);

/// <summary>
///	Stop the motor
///	</summary>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// Calling piHaltMotor() will stop the motor from moving and will abort
/// any ongoing homing operation.
/// @sa ::piRunMotorToPosition()
/// @sa ::piHomeMotor()
/// </remarks>
int __stdcall piHaltMotor(PIHANDLE handle);

/// <summary>
///	Initiate homing the motor.
///	</summary>
///	<param name="Velocity"><c>[in]</c> The @ref MotorVelocity "motor velocity"
/// to use during homing (1 to 12).</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// The system will initiate a search for the home switch. This function does not wait
/// for homing to complete.
/// </para>
/// <para>
/// The motor will move in the negative direction and look for the home switch to turn on.
/// If the home switch is missing or fails, the home operation will continue until you
/// call ::piHaltMotor().
/// </para>
/// <para>
/// The home position is not established until you initiate a move to a
/// positive (non-zero) position after finding the home switch location.
/// After finding the home switch the motor sets the position zero.
/// When you subsequently initiate a move to a positive (non-zero) position, the motor
/// will keep the reported position at zero while it moves until the home switch turns
/// off. It then set that position as the zero position.
/// </para>
/// @sa @ref MotorVelocity "Motor Velocity"
/// @sa ::piRunMotorToPosition()
/// </remarks>
int __stdcall piHomeMotor(int Velocity, PIHANDLE handle);

/// <summary>
///	Initiate a move to a destination position.
///	</summary>
///	<param name="Destination"><c>[in]</c> The destination @ref MotorPosition
/// "motor position".</param>
///	<param name="Velocity"><c>[in]</c> The @ref MotorVelocity "motor velocity"
/// to use during the move (1 to 12).</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// The system will initiate a move to the specified @p Destination position at
/// the specified @p Velocity. This function does not wait for the move to complete.
/// </para>
/// <para>
/// The destination position can be any position between 1 and 2<sup>31</sup>-1, but the
/// physical upper limit depends on the device. See @ref MotorPosition "Motor Position".
/// </para>
/// @sa @ref MotorPosition "Motor Position"
/// @sa @ref MotorVelocity "Motor Velocity"
/// </remarks>
int __stdcall piRunMotorToPosition( int Destination, int Velocity, PIHANDLE handle);

/// <summary>
///	Set the velocity of the motor.
///	</summary>
///	<param name="Velocity"><c>[in]</c> The velocity of the motor.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// @par Deprecated
/// <para>
/// This function is deprecated and may be removed from future versions
/// of the library.
/// </para>
/// @par
/// <para>
/// In theory, this function changes the velocity of the motor.
/// However, the motor device does not permit changing velocity on the fly.
/// You must first call ::piHaltMotor() to stop the motor, and then issue a new
/// ::piRunMotorToPosition() and where you specify the new destination
/// and velocity.
/// Setting the velocity with this function is effectively meaningless.
/// </para>
/// @sa @ref MotorVelocity "Motor Velocity"
/// @sa ::piRunMotorToPosition()
/// @sa ::piHomeMotor()
/// </remarks>
int __stdcall piSetMotorVelocity(int Velocity, PIHANDLE handle);

/** @} */ // end of MotorFunctions group

/**
	@defgroup ShutterFunctions Shutter Functions
	Functions to control USB Shutter devices
	@{
*/

/** @defgroup ShutterConstants Shutter Constants
	State of the Shutter
	@{
*/

///	<summary>
///	Shutter is closed.
///	</summary>
#define PI_SHUTTER_CLOSED 0

///	<summary>
///	Shutter is open.
///	</summary>
#define PI_SHUTTER_OPEN 1

/** @} */ // end of ShutterConstants group

/// <summary>
///	Search for connected USB Shutter devices
///	</summary>
///	<param name="DeviceCount"><c>[out]</c> The number of devices found. This is the number
/// of values returned in @p SerialNumberArray.</param>
///	<param name="SerialNumberArray"><c>[in/out]</c> An array of
/// device serial numbers. It must be pre-allocated to be @p ArraySize
/// in length. It will be returned with @p DeviceCount values set.
/// </param>
///	<param name="ArraySize"><c>[in]</c> The size of the
/// @p SerialNumberArray arrays as passed into this function.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// Searches for connected Picard Industries Shutter devices, and returns an array of
/// Serial Numbers.
/// @sa @ref Discovery
/// </remarks>
int __stdcall piFindShutters(int* DeviceCount, int* SerialNumberArray, int ArraySize);

/// <summary>
///	Connect to a USB Shutter.
///	</summary>
///	<param name="ErrorNumber"><c>[out]</c> An @ref ErrorNumbers "error number".</param>
///	<param name="SerialNum"><c>[in]</c> The device serial number.</param>
///	<returns>The device handle for the new device. If the device is not found or an
/// error occurs, NULL is returned.</returns>
/// <remarks>
/// @sa ::piDisconnectShutter()
/// </remarks>
PIHANDLE __stdcall piConnectShutter(int * ErrorNumber, int SerialNum);

/// <summary>
///	Disconnect from a USB Shutter.
///	</summary>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// @sa ::piConnectShutter()
/// </remarks>
void __stdcall piDisconnectShutter(PIHANDLE handle);

/// <summary>
///	Get the shutter state.
///	</summary>
///	<param name="ShutterState"><c>[out]</c> The current state of the shutter.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// The shutter state will be returned as one of:
/// </para>
/// <list type="bullet">
///   <item>#PI_SHUTTER_OPEN</item>
///   <item>#PI_SHUTTER_CLOSED</item>
/// </list>
/// <para>
/// Immediately after powering up the shutter, the shutter will be closed.
/// </para>
/// <para>
/// The shutter device does not contain a sensor and the shutter state reflects the
/// most recent state commanded with ::piSetShutterState(). If the shutter is physically
/// blocked from moving, or you manually move the shutter, piGetShutterState will
/// return the commanded state and not the actual state.
/// </para>
/// @sa ::piSetShutterState()
/// </remarks>
int __stdcall piGetShutterState(int * ShutterState, PIHANDLE handle);

/// <summary>
///	Set the shutter state.
///	</summary>
///	<param name="ShutterState"><c>[in]</c> The state of the shutter to set.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// The shutter will be set to the specified state.
/// Valid values are:
/// </para>
/// <list type="bullet">
///   <item>#PI_SHUTTER_CLOSED</item>
///   <item>#PI_SHUTTER_OPEN</item>
/// </list>
/// @sa ::piGetShutterState()
/// </remarks>
int __stdcall piSetShutterState(int ShutterState, PIHANDLE handle);

/** @} */ // end of ShutterFunctions group


/**
	@defgroup RelayFunctions Relay Functions
	Functions to control USB Relay devices
	@{
*/

/// <summary>
///	Search for connected USB Relay devices
///	</summary>
///	<param name="DeviceCount"><c>[out]</c> The number of devices found. This is the number
/// of values returned in @p SerialNumberArray.</param>
///	<param name="SerialNumberArray"><c>[in/out]</c> An array of
/// device serial numbers. It must be pre-allocated to be @p ArraySize
/// in length. It will be returned with @p DeviceCount values set.
/// </param>
///	<param name="ArraySize"><c>[in]</c> The size of the
/// @p SerialNumberArray arrays as passed into this function.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// Searches for connected Picard Industries Relay devices, and returns an array of
/// Serial Numbers.
///
/// Note that Relay and Valve devices share the same ProductID, and are therefore not
/// distinguishable. This function will return Relay and Valve devices.
/// @sa @ref Discovery
/// </remarks>
int __stdcall piFindRelays(int* DeviceCount, int* SerialNumberArray, int ArraySize);

/// <summary>
///	Connect to a USB Relay.
///	</summary>
///	<param name="ErrorNumber"><c>[out]</c> An @ref ErrorNumbers "error number".</param>
///	<param name="SerialNum"><c>[in]</c> The device serial number.</param>
///	<returns>The device handle for the new device. If the device is not found or an
/// error occurs, NULL is returned.</returns>
/// <remarks>
/// @sa ::piDisconnectRelay()
/// </remarks>
PIHANDLE __stdcall piConnectRelay(int * ErrorNumber, int SerialNum);

/// <summary>
///	Disconnect from a USB Relay.
///	</summary>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// @sa ::piConnectRelay()
/// </remarks>
void __stdcall piDisconnectRelay(PIHANDLE handle);

/// <summary>
///	Get the state of the relays.
///	</summary>
///	<param name="RelayStates"><c>[out]</c> The current state of the relays.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// @p RelayStates will be returned with a bit for each relay.
/// Bit 0, the low order bit, corresponds to relay 1.
/// Bit 1 corresponds to relay 2, etc.
/// The bit will be 1 when the relay is ON (energized), and will be 0 when the relay
/// is OFF (de-energized).
/// </para>
/// <para>
/// Immediately after powering up the Relay device, all relays are OFF (de-energized).
/// </para>
/// @sa ::piSetRelayStates()
/// </remarks>
int __stdcall piGetRelayStates(int * RelayStates, PIHANDLE handle);

/// <summary>
///	Set the state of the relays.
///	</summary>
///	<param name="RelayStates"><c>[in]</c> The desired state of the relays.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// @p RelayStates contains a bit for each relay.
/// Bit 0, the low order bit, corresponds to relay 1.
/// Bit 1 corresponds to relay 2, etc.
/// The bit should be 1 when the relay is set ON (energized), and should be 0
/// when the relay is set OFF (de-energized).
/// </para>
/// <para>
/// Immediately after powering up the Relay device, all relays are OFF (de-energized).
/// </para>
/// @sa ::piGetRelayStates()
/// </remarks>
int __stdcall piSetRelayStates(int RelayStates, PIHANDLE handle);

/** @} */ // end of RelayFunctions group

/**
	@defgroup RotatorFunctions Rotator Functions
	Functions to control USB Rotator devices
    You can also connect to and control Rotator devices using the
    @ref GradientFunctions.
	@{
*/

/// <summary>
///	Search for connected USB Rotator devices
///	</summary>
///	<param name="DeviceCount"><c>[out]</c> The number of devices found. This is the number
/// of values returned in @p SerialNumberArray.</param>
///	<param name="SerialNumberArray"><c>[in/out]</c> An array of
/// device serial numbers. It must be pre-allocated to be @p ArraySize
/// in length. It will be returned with @p DeviceCount values set.
/// </param>
///	<param name="ArraySize"><c>[in]</c> The size of the
/// @p SerialNumberArray arrays as passed into this function.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// Searches for connected Picard Industries Rotator devices, and returns an array of
/// Serial Numbers.
///
/// Note that Filter Wheel, Gradient Wheel, and Rotator devices share the same ProductID, and
/// are therefore not distinguishable. This function will return all Filter Wheel,
/// Gradient Wheel, and Rotator devices.
/// @sa @ref Discovery
/// </remarks>
int __stdcall piFindRotators(int* DeviceCount, int* SerialNumberArray, int ArraySize);

/// <summary>
///	Connect to a USB Rotator.
///	</summary>
///	<param name="ErrorNumber"><c>[out]</c> An @ref ErrorNumbers "error number".</param>
///	<param name="SerialNum"><c>[in]</c> The device serial number.</param>
///	<returns>The device handle for the new device. If the device is not found or an
/// error occurs, NULL is returned.</returns>
/// <remarks>
/// @sa ::piDisconnectRotator()
/// </remarks>
PIHANDLE __stdcall piConnectRotator(int * ErrorNumber, int SerialNum);

/// <summary>
///	Disconnect from a USB Rotator.
///	</summary>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// @sa ::piConnectRotator()
/// </remarks>
void __stdcall piDisconnectRotator(PIHANDLE handle);

/// <summary>
///	Get the rotator position.
///	</summary>
///	<param name="Position"><c>[out]</c> The current position of the rotator.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// The reported position will be between 1 and 1023.
/// </para>
/// @sa ::piSetRotatorPosition()
/// </remarks>
int __stdcall piGetRotatorPosition(int * Position, PIHANDLE handle);

/// <summary>
///	Initiate a move to a new rotator position.
///	</summary>
///	<param name="Destination"><c>[in]</c> The destination position of the rotator.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// The destination position should be between 1 and 1023.
/// </para>
/// <para>
/// Setting the position to 0 will cause the rotator to stop immediately.
/// </para>
/// @sa ::piGetRotatorPosition()
/// </remarks>
int __stdcall piSetRotatorPosition(int Destination, PIHANDLE handle);

/** @} */ // end of RotatorFunctions group

/**
	@defgroup TwisterFunctions Twister Functions
	Functions to control USB Twister devices

    @anchor TwisterPosition
    @par USB Twister Position

    The USB Twister uses a stepper motor to rotate a shaft. You command the motor to move
    to a new position with the ::piRunTwisterToPosition() function, specifying the
    destination position in steps (or counts). There are 200 steps for each revolution of
    the shaft, so each step corresponds to 1.8 degrees. You can specify any position
    between -32767 and +32767. If you specify a position less than -32767, the motor will
    move to position -32767. Similarly, if you specify a position greater than +32767, the
    motor will move to position +32767.

    You can read the current position at any time (while moving or not) with the
    ::piGetTwisterPosition(), ::piGetTwisterStatus(), and ::piGetTwisterStatusEx()
    functions. You can reset the position to zero with the ::piSetTwisterPositionZero()
    function.

    You can command the motor to move continuously in either the positive or negative
    direction with the ::piRunTwisterContinuous() function. When you issue this command,
    the position is set to zero and remains there during the continuous move. You can
    leave the motor running for as long as you wish.

    The positive direction (increasing counts) is counter-clockwise rotation if you are looking at the USB
    Twister from the shaft end.

    @anchor TwisterVelocity
    @par USB Twister Velocity

    The ::piRunTwisterToPosition() and ::piRunTwisterContinuous() functions let you
    specify the move velocity. The velocity is a number between 1 and 13, where 1 is the
    slowest speed and 13 is the highest speed.

    We recommend that you limit your velocity to be 10 or less. These velocities should
    work well with most devices you connect to the Twister. If your load is small and
    light, you may be able to use some or all of the faster velocities between 11 and 13.
    If you attempt to move too large a load at too high a speed, the motor may stall, or
    may miss steps and not move the full distance.

    The following table shows the velocity settings and the approximate speed they correspond to.

    Velocity  | Steps/sec  | Degrees/Sec | RPM
    :-------: | :--------: | :---------: | :----:
    1         | 133        | 240         | 40
    2         | 143        | 257         | 43
    3         | 154        | 277         | 46
    4         | 167        | 300         | 50
    5         | 182        | 328         | 55
    6         | 200        | 360         | 60
    7         | 222        | 400         | 67
    8         | 250        | 450         | 75
    9         | 286        | 514         | 86
    10        | 333        | 600         | 100
    11        | 400        | 720         | 120
    12        | 500        | 900         | 150
    13        | 667        | 1200        | 200

    @anchor TwisterSensorPosition
    @par USB Twister Sensor Position

    Some versions of the Twister include an analog sensor which can be used to read a
    position. This is an option that can be ordered with the device. It is automatically
    included on versions of the twister used in the USB ZTable product.

    The position is a 10 bit value (0 to 1023) returned from the A/D converter on the
    board. It reads the value of a potentiometer which is attached to the rotary stage.
    The sensor position does not have as much resolution as the motor steps, but it is
    absolute rather than relative to the power-on or user set zero position.

    The ::piGetTwisterSensorPosition() and ::piGetTwisterStatusEx() functions return the
    value of this sensor.

	@{
*/

/// <summary>
///	Search for connected USB Twister devices
///	</summary>
///	<param name="DeviceCount"><c>[out]</c> The number of devices found. This is the number
/// of values returned in @p SerialNumberArray.</param>
///	<param name="SerialNumberArray"><c>[in/out]</c> An array of
/// device serial numbers. It must be pre-allocated to be @p ArraySize
/// in length. It will be returned with @p DeviceCount values set.
/// </param>
///	<param name="ArraySize"><c>[in]</c> The size of the
/// @p SerialNumberArray arrays as passed into this function.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// Searches for connected Picard Industries Twister devices, and returns an array of
/// Serial Numbers.
/// @sa @ref Discovery
/// </remarks>
int __stdcall piFindTwisters(int* DeviceCount, int* SerialNumberArray, int ArraySize);

// USB Twister Functions
/// <summary>
///	Connect to a USB Twister.
///	</summary>
///	<param name="ErrorNumber"><c>[out]</c> An @ref ErrorNumbers "error number".</param>
///	<param name="SerialNum"><c>[in]</c> The device serial number.</param>
///	<returns>The device handle for the new device. If the device is not found or an
/// error occurs, NULL is returned.</returns>
/// <remarks>
/// @sa ::piDisconnectTwister()
/// </remarks>
PIHANDLE __stdcall piConnectTwister(int * ErrorNumber, int SerialNum);

/// <summary>
///	Disconnect from a USB Twister.
///	</summary>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// @sa ::piConnectTwister()
/// </remarks>
void __stdcall piDisconnectTwister(PIHANDLE handle);

/// <summary>
///	Get a value indicating whether the twister is moving.
///	</summary>
///	<param name="Moving"><c>[out]</c> @p TRUE if the twister is moving, @p FALSE otherwise.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// @sa ::piRunTwisterToPosition()
/// </remarks>
int __stdcall piGetTwisterMovingStatus(BOOL * Moving, PIHANDLE handle);

/// <summary>
///	Get the position of the twister.
///	</summary>
///	<param name="Position"><c>[out]</c> The current position of the twister.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// The @p Position is a value between -32767 and +32767.
/// See @ref TwisterPosition "Twister Position".
/// </para>
/// @sa @ref TwisterPosition "Twister Position"
/// @sa ::piRunTwisterToPosition()
/// @sa ::piRunTwisterContinuous()
/// </remarks>
int __stdcall piGetTwisterPosition(int * Position, PIHANDLE handle);

/// <summary>
///	Get the position of the twister sensor.
///	</summary>
///	<param name="SensorPosition"><c>[out]</c> The current position of the twister sensor.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// The @p SensorPosition is a value between 0 and 1023.
/// See @ref TwisterSensorPosition "Twister SensorPosition".
/// </para>
/// @sa @ref TwisterSensorPosition "Twister Sensor Position"
/// @sa ::piGetTwisterStatusEx()
/// @sa ::piRunTwisterToPosition()
/// @sa ::piRunTwisterContinuous()
/// </remarks>
int __stdcall piGetTwisterSensorPosition(int* SensorPosition, PIHANDLE handle);

/// <summary>
///	Get the position and status of the twister.
///	</summary>
///	<param name="Position"><c>[out]</c> The current position of the twister.</param>
///	<param name="Moving"><c>[out]</c> @p TRUE if the twister is moving, @p FALSE otherwise.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// This method gets the current twister position and status in a single function call.
/// It returns the value of the ::piGetTwisterPosition() and ::piGetTwisterMovingStatus()
/// functions.
/// </para>
/// <para>
/// It is more efficient to call this function rather than calling 2 separate functions.
/// Using this method reduces I/O traffic to the device and can improve the responsiveness
/// of your application.
/// </para>
/// <para>
/// The @p Position is a value between -32767 and +32767.
/// See @ref TwisterPosition "Twister Position".
/// </para>
/// @sa @ref TwisterPosition "Twister Position"
/// @sa ::piGetTwisterStatusEx()
/// @sa ::piRunTwisterToPosition()
/// @sa ::piRunTwisterContinuous()
/// </remarks>
int __stdcall piGetTwisterStatus(int * Position, BOOL* Moving, PIHANDLE handle);

/// <summary>
///	Get the position and status of the twister.
///	</summary>
///	<param name="Position"><c>[out]</c> The current position of the twister.</param>
///	<param name="SensorPosition"><c>[out]</c> The current position of the twister sensor.</param>
///	<param name="Moving"><c>[out]</c> @p TRUE if the twister is moving, @p FALSE otherwise.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// This method gets the current twister position and status in a single function call.
/// It returns the value of the ::piGetTwisterPosition(), ::piGetTwisterSensorPosition(), and
/// ::piGetTwisterMovingStatus() functions.
/// </para>
/// <para>
/// It is more efficient to call this function rather than calling 3 separate functions.
/// Using this method reduces I/O traffic to the device and can improve the responsiveness
/// of your application.
/// </para>
/// <para>
/// The @p Position is a value between -32767 and +32767.
/// See @ref TwisterPosition "Twister Position".
/// </para>
/// <para>
/// The @p SensorPosition is a value between 0 and 1023.
/// See @ref TwisterSensorPosition "Twister Sensor Position".
/// </para>
/// @sa @ref TwisterPosition "Twister Position"
/// @sa @ref TwisterSensorPosition "Twister Sensor Position"
/// @sa ::piGetTwisterStatus()
/// @sa ::piRunTwisterToPosition()
/// @sa ::piRunTwisterContinuous()
/// </remarks>
int __stdcall piGetTwisterStatusEx(int* Position, int* SensorPosition, BOOL* Moving, PIHANDLE handle);

/// <summary>
///	Get the velocity of the twister.
///	</summary>
///	<param name="Velocity"><c>[out]</c> The velocity of the twister.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// @sa @ref TwisterVelocity "Twister Velocity"
/// @sa ::piRunTwisterToPosition()
/// @sa ::piRunTwisterContinuous()
/// </remarks>
int __stdcall piGetTwisterVelocity(int * Velocity, PIHANDLE handle);

/// <summary>
///	Stop the twister
///	</summary>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// Calling piHaltTwister() will stop the twister from moving.
/// @sa ::piRunTwisterToPosition()
/// </remarks>
int __stdcall piHaltTwister(PIHANDLE handle);

/// <summary>
///	Start the Twister moving continuously.
///	</summary>
///	<param name="Direction"><c>[in]</c> The direction to move. Specify +1 (or larger)
/// for motion in the positive direction. Specify 0 or any negative value for motion
/// in the negative direction.</param>
///	<param name="Velocity"><c>[in]</c> The @ref TwisterVelocity "twister velocity"
/// to use during the move (1 to 13).</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// The twister position will be set to zero and will remain at zero during
/// continuous motion.
/// </para>
/// @sa @ref TwisterVelocity "Twister Velocity"
/// </remarks>
int __stdcall piRunTwisterContinuous( int Direction, int Velocity, PIHANDLE handle);

/// <summary>
///	Initiate a move to a destination position.
///	</summary>
///	<param name="Destination"><c>[in]</c> The destination @ref TwisterPosition
/// "twister position".</param>
///	<param name="Velocity"><c>[in]</c> The @ref TwisterVelocity "twister velocity"
/// to use during the move (1 to 13).</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// The system will initiate a move to the specified @p Destination position at
/// the specified @p Velocity. This function does not wait for the move to complete.
/// </para>
/// <para>
/// The destination position can be any position between -32767 and +32767.
/// See @ref TwisterPosition "Twister Position".
/// </para>
/// @sa @ref TwisterPosition "Twister Position"
/// @sa @ref TwisterVelocity "Twister Velocity"
/// </remarks>
int __stdcall piRunTwisterToPosition( int Destination, int Velocity, PIHANDLE handle);

/// <summary>
///	Set the twister position to zero.
///	</summary>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// Sets the current position to zero.
/// </para>
/// <para>
/// If the twister is moving, it will be halted before setting the position to zero.
/// </para>
/// </remarks>
/// @sa @ref TwisterPosition "Twister Position"
int __stdcall piSetTwisterPositionZero(PIHANDLE handle);

/** @} */ // end of TwisterFunctions group

/**
	@defgroup ValveFunctions Valve Functions
	Functions to control USB Valve devices
	@{
*/

/// <summary>
///	Search for connected USB Valve devices
///	</summary>
///	<param name="DeviceCount"><c>[out]</c> The number of devices found. This is the number
/// of values returned in @p SerialNumberArray.</param>
///	<param name="SerialNumberArray"><c>[in/out]</c> An array of
/// device serial numbers. It must be pre-allocated to be @p ArraySize
/// in length. It will be returned with @p DeviceCount values set.
/// </param>
///	<param name="ArraySize"><c>[in]</c> The size of the
/// @p SerialNumberArray arrays as passed into this function.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// Searches for connected Picard Industries Valve devices, and returns an array of
/// Serial Numbers.
///
/// Note that Relay and Valve devices share the same ProductID, and are therefore not
/// distinguishable. This function will return Relay and Valve devices.
/// @sa @ref Discovery
/// </remarks>
int __stdcall piFindValves(int* DeviceCount, int* SerialNumberArray, int ArraySize);

/// <summary>
///	Connect to a USB Valve.
///	</summary>
///	<param name="ErrorNumber"><c>[out]</c> An @ref ErrorNumbers "error number".</param>
///	<param name="SerialNum"><c>[in]</c> The device serial number.</param>
///	<returns>The device handle for the new device. If the device is not found or an
/// error occurs, NULL is returned.</returns>
/// <remarks>
/// @sa ::piDisconnectValve()
/// </remarks>
PIHANDLE __stdcall piConnectValve(int * ErrorNumber, int SerialNum);

/// <summary>
///	Disconnect from a USB Valve.
///	</summary>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// @sa ::piConnectValve()
/// </remarks>
void __stdcall piDisconnectValve(PIHANDLE handle);

/// <summary>
///	Get the state of the sensor.
///	</summary>
///	<param name="SensorValue"><c>[out]</c> The current value of the sensor,
/// in the range 0 to 1023.
/// The meaning of this value depends on what sensor you have attached to the device.
/// </param>
///	<param name="SensorNumber"><c>[in]</c> The sensor number you want to read.
/// A value of 0 corresponds to sensor 1 and a value of 1 corresponds to sensor 2.
/// </param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
int __stdcall piGetValveSensor(int * SensorValue, int SensorNumber, PIHANDLE handle);

/// <summary>
///	Get the state of the valves.
///	</summary>
///	<param name="ValveStates"><c>[out]</c> The current state of the valves.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// @p ValveStates will be returned with a bit for each valve.
/// Bit 0, the low order bit, corresponds to valve 1.
/// Bit 1 corresponds to valve 2, etc.
/// The bit will be 1 when the valve is ON (relay energized), and will be 0 when
/// the valve is OFF (relay de-energized).
/// </para>
/// <para>
/// Immediately after powering up the Valve device, all valves are OFF (relay de-energized).
/// </para>
/// @sa ::piSetValveStates()
/// </remarks>
int __stdcall piGetValveStates(int * ValveStates, PIHANDLE handle);

/// <summary>
///	Set the state of the valves.
///	</summary>
///	<param name="ValveStates"><c>[in]</c> The desired state of the valves.</param>
///	<param name="handle"><c>[in]</c> The device handle.</param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// <para>
/// @p ValveStates contains a bit for each valve.
/// Bit 0, the low order bit, corresponds to valve 1.
/// Bit 1 corresponds to valve 2, etc.
/// The bit should be 1 when the valve is set ON (relay energized), and should be 0
/// when the valve is set OFF (relay de-energized).
/// </para>
/// <para>
/// Immediately after powering up the Valve device, all valves are OFF (relay de-energized).
/// </para>
/// @sa ::piGetValveStates()
/// </remarks>
int __stdcall piSetValveStates(int ValveStates, PIHANDLE handle);

/** @} */ // end of ValveFunctions group

/**
	@defgroup AllDevices All Device
	Functions to search for all devices
	@{
*/

/// <summary>
///	Search for connected Picard Industries devices
///	</summary>
///	<param name="DeviceCount"><c>[out]</c> The number of devices found. This is the number
/// of values returned in @p ProductIdArray and @p SerialNumberArray.</param>
///	<param name="ProductIDArray"><c>[in/out]</c> An array of
/// @ref ProductID "ProductID numbers". It must be pre-allocated to be @p ArraySize
/// in length. It will be returned with @p DeviceCount values set.
/// </param>
///	<param name="SerialNumberArray"><c>[in/out]</c> An array of
/// device serial numbers. It must be pre-allocated to be @p ArraySize
/// in length. It will be returned with @p DeviceCount values set.
/// </param>
///	<param name="ArraySize"><c>[in]</c> The size of the @p ProductIDArray and
/// @p SerialNumberArray arrays as passed into this function.
/// </param>
///	<param name="DesiredProductID"><c>[in]</c> The @ref ProductID "ProductID" of the
/// type of product to search for.
/// </param>
///	<returns>An @ref ErrorNumbers "error number".</returns>
/// <remarks>
/// Searches for connected Picard Industries devices with a given
/// @ref ProductID "ProductID".
/// Returns arrays of Product IDs and Serial Numbers.
///
/// Specify @ref PRODUCT_ID_ALL for the @p DesiredProductID to search for
/// all Picard Industries products.
/// @sa @ref Discovery
/// </remarks>
int __stdcall piFindDevices(int* DeviceCount, int* ProductIDArray, int* SerialNumberArray,
         int ArraySize, int DesiredProductID);

/** @} */ // end of AllDevices group

#ifdef __cplusplus
}
#endif

#endif  // PIUSB_H

