
cdef extern from "./include/atmcdLXd.h":
    
    ctypedef long at_32
    ctypedef long at_u32

    unsigned int Initialize(char * dir)
    unsigned int ShutDown()

    unsigned int CoolerON()
    unsigned int CoolerOFF()
    unsigned int SetTemperature(int temperature)
    unsigned int GetTemperature(int * temperature)
    unsigned int GetTemperatureRange(int * mintemp, int * maxtemp)


    unsigned int SetShutter(int typ, int mode, int closingtime, int openingtime)
    unsigned int SetAcquisitionMode(int mode)
    unsigned int SetReadMode(int mode)
    unsigned int SetExposureTime(float time)
    unsigned int SetImage(int hbin, int vbin, int hstart, int hend, int vstart, int vend)

    unsigned int StartAcquisition()
    unsigned int GetStatus(int * status)
    
    unsigned int GetAcquiredData(at_32 * arr, at_u32 size)
    unsigned int GetMostRecentImage(at_32 * arr, at_u32 size)

    cdef int DRV_ERROR_CODES
    cdef int DRV_SUCCESS
    cdef int DRV_VXDNOTINSTALLED
    cdef int DRV_ERROR_SCAN
    cdef int DRV_ERROR_CHECK_SUM
    cdef int DRV_ERROR_FILELOAD
    cdef int DRV_UNKNOWN_FUNCTION
    cdef int DRV_ERROR_VXD_INIT
    cdef int DRV_ERROR_ADDRESS
    cdef int DRV_ERROR_PAGELOCK
    cdef int DRV_ERROR_PAGEUNLOCK
    cdef int DRV_ERROR_BOARDTEST
    cdef int DRV_ERROR_ACK
    cdef int DRV_ERROR_UP_FIFO
    cdef int DRV_ERROR_PATTERN

    cdef int DRV_ACQUISITION_ERRORS
    cdef int DRV_ACQ_BUFFER
    cdef int DRV_ACQ_DOWNFIFO_FULL
    cdef int DRV_PROC_UNKONWN_INSTRUCTION
    cdef int DRV_ILLEGAL_OP_CODE
    cdef int DRV_KINETIC_TIME_NOT_MET
    cdef int DRV_ACCUM_TIME_NOT_MET
    cdef int DRV_NO_NEW_DATA
    cdef int KERN_MEM_ERROR
    cdef int DRV_SPOOLERROR
    cdef int DRV_SPOOLSETUPERROR
    cdef int DRV_FILESIZELIMITERROR
    cdef int DRV_ERROR_FILESAVE

    cdef int DRV_TEMPERATURE_CODES
    cdef int DRV_TEMPERATURE_OFF
    cdef int DRV_TEMPERATURE_NOT_STABILIZED
    cdef int DRV_TEMPERATURE_STABILIZED
    cdef int DRV_TEMPERATURE_NOT_REACHED
    cdef int DRV_TEMPERATURE_OUT_RANGE
    cdef int DRV_TEMPERATURE_NOT_SUPPORTED
    cdef int DRV_TEMPERATURE_DRIFT

    cdef int DRV_TEMP_CODES
    cdef int DRV_TEMP_OFF
    cdef int DRV_TEMP_NOT_STABILIZED
    cdef int DRV_TEMP_STABILIZED
    cdef int DRV_TEMP_NOT_REACHED
    cdef int DRV_TEMP_OUT_RANGE
    cdef int DRV_TEMP_NOT_SUPPORTED
    cdef int DRV_TEMP_DRIFT

    cdef int DRV_GENERAL_ERRORS
    cdef int DRV_INVALID_AUX
    cdef int DRV_COF_NOTLOADED
    cdef int DRV_FPGAPROG
    cdef int DRV_FLEXERROR
    cdef int DRV_GPIBERROR
    cdef int DRV_EEPROMVERSIONERROR

    cdef int DRV_DATATYPE
    cdef int DRV_DRIVER_ERRORS
    cdef int DRV_P1INVALID
    cdef int DRV_P2INVALID
    cdef int DRV_P3INVALID
    cdef int DRV_P4INVALID
    cdef int DRV_INIERROR
    cdef int DRV_COFERROR
    cdef int DRV_ACQUIRING
    cdef int DRV_IDLE
    cdef int DRV_TEMPCYCLE
    cdef int DRV_NOT_INITIALIZED
    cdef int DRV_P5INVALID
    cdef int DRV_P6INVALID
    cdef int DRV_INVALID_MODE
    cdef int DRV_INVALID_FILTER

    cdef int DRV_I2CERRORS
    cdef int DRV_I2CDEVNOTFOUND
    cdef int DRV_I2CTIMEOUT
    cdef int DRV_P7INVALID
    cdef int DRV_P8INVALID
    cdef int DRV_P9INVALID
    cdef int DRV_P10INVALID
    cdef int DRV_P11INVALID

    cdef int DRV_USBERROR
    cdef int DRV_IOCERROR
    cdef int DRV_VRMVERSIONERROR
    cdef int DRV_GATESTEPERROR
    cdef int DRV_USB_INTERRUPT_ENDPOINT_ERROR
    cdef int DRV_RANDOM_TRACK_ERROR
    cdef int DRV_INVALID_TRIGGER_MODE
    cdef int DRV_LOAD_FIRMWARE_ERROR
    cdef int DRV_DIVIDE_BY_ZERO_ERROR
    cdef int DRV_INVALID_RINGEXPOSURES
    cdef int DRV_BINNING_ERROR
    cdef int DRV_INVALID_AMPLIFIER
    cdef int DRV_INVALID_COUNTCONVERT_MODE
    cdef int DRV_USB_INTERRUPT_ENDPOINT_TIMEOUT

    cdef int DRV_ERROR_NOCAMERA
    cdef int DRV_NOT_SUPPORTED
    cdef int DRV_NOT_AVAILABLE

    cdef int DRV_ERROR_MAP
    cdef int DRV_ERROR_UNMAP
    cdef int DRV_ERROR_MDL
    cdef int DRV_ERROR_UNMDL
    cdef int DRV_ERROR_BUFFSIZE
    cdef int DRV_ERROR_NOHANDLE

    cdef int DRV_GATING_NOT_AVAILABLE
    cdef int DRV_FPGA_VOLTAGE_ERROR

    cdef int DRV_OW_CMD_FAIL
    cdef int DRV_OWMEMORY_BAD_ADDR
    cdef int DRV_OWCMD_NOT_AVAILABLE
    cdef int DRV_OW_NO_SLAVES
    cdef int DRV_OW_NOT_INITIALIZED
    cdef int DRV_OW_ERROR_SLAVE_NUM
    cdef int DRV_MSTIMINGS_ERROR

    cdef int DRV_OA_NULL_ERROR
    cdef int DRV_OA_PARSE_DTD_ERROR
    cdef int DRV_OA_DTD_VALIDATE_ERROR
    cdef int DRV_OA_FILE_ACCESS_ERROR
    cdef int DRV_OA_FILE_DOES_NOT_EXIST
    cdef int DRV_OA_XML_INVALID_OR_NOT_FOUND_ERROR
    cdef int DRV_OA_PRESET_FILE_NOT_LOADED
    cdef int DRV_OA_USER_FILE_NOT_LOADED
    cdef int DRV_OA_PRESET_AND_USER_FILE_NOT_LOADED
    cdef int DRV_OA_INVALID_FILE
    cdef int DRV_OA_FILE_HAS_BEEN_MODIFIED
    cdef int DRV_OA_BUFFER_FULL
    cdef int DRV_OA_INVALID_STRING_LENGTH
    cdef int DRV_OA_INVALID_CHARS_IN_NAME
    cdef int DRV_OA_INVALID_NAMING
    cdef int DRV_OA_GET_CAMERA_ERROR
    cdef int DRV_OA_MODE_ALREADY_EXISTS
    cdef int DRV_OA_STRINGS_NOT_EQUAL
    cdef int DRV_OA_NO_USER_DATA
    cdef int DRV_OA_VALUE_NOT_SUPPORTED
    cdef int DRV_OA_MODE_DOES_NOT_EXIST
    cdef int DRV_OA_CAMERA_NOT_SUPPORTED
    cdef int DRV_OA_FAILED_TO_GET_MODE
    cdef int DRV_OA_CAMERA_NOT_AVAILABLE

    cdef int DRV_PROCESSING_FAILED
