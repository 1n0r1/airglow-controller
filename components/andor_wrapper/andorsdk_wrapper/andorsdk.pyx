cimport andorsdk

from cython.operator import dereference
from libc.stdlib cimport malloc, free
import numpy as np

errorcodes = [
    [DRV_ERROR_CODES, "DRV_ERROR_CODES"],
    [DRV_SUCCESS, "DRV_SUCCESS"],
    [DRV_VXDNOTINSTALLED, "DRV_VXDNOTINSTALLED"],
    [DRV_ERROR_SCAN, "DRV_ERROR_SCAN"],
    [DRV_ERROR_CHECK_SUM, "DRV_ERROR_CHECK_SUM"],
    [DRV_ERROR_FILELOAD, "DRV_ERROR_FILELOAD"],
    [DRV_UNKNOWN_FUNCTION, "DRV_UNKNOWN_FUNCTION"],
    [DRV_ERROR_VXD_INIT, "DRV_ERROR_VXD_INIT"],
    [DRV_ERROR_ADDRESS, "DRV_ERROR_ADDRESS"],
    [DRV_ERROR_PAGELOCK, "DRV_ERROR_PAGELOCK"],
    [DRV_ERROR_PAGEUNLOCK, "DRV_ERROR_PAGEUNLOCK"],
    [DRV_ERROR_BOARDTEST, "DRV_ERROR_BOARDTEST"],
    [DRV_ERROR_ACK, "DRV_ERROR_ACK"],
    [DRV_ERROR_UP_FIFO, "DRV_ERROR_UP_FIFO"],
    [DRV_ERROR_PATTERN, "DRV_ERROR_PATTERN"],
    [DRV_ACQUISITION_ERRORS, "DRV_ACQUISITION_ERRORS"],
    [DRV_ACQ_BUFFER, "DRV_ACQ_BUFFER"],
    [DRV_ACQ_DOWNFIFO_FULL, "DRV_ACQ_DOWNFIFO_FULL"],
    [DRV_PROC_UNKONWN_INSTRUCTION, "DRV_PROC_UNKONWN_INSTRUCTION"],
    [DRV_ILLEGAL_OP_CODE, "DRV_ILLEGAL_OP_CODE"],
    [DRV_KINETIC_TIME_NOT_MET, "DRV_KINETIC_TIME_NOT_MET"],
    [DRV_ACCUM_TIME_NOT_MET, "DRV_ACCUM_TIME_NOT_MET"],
    [DRV_NO_NEW_DATA, "DRV_NO_NEW_DATA"],
    [KERN_MEM_ERROR, "KERN_MEM_ERROR"],
    [DRV_SPOOLERROR, "DRV_SPOOLERROR"],
    [DRV_SPOOLSETUPERROR, "DRV_SPOOLSETUPERROR"],
    [DRV_FILESIZELIMITERROR, "DRV_FILESIZELIMITERROR"],
    [DRV_ERROR_FILESAVE, "DRV_ERROR_FILESAVE"],
    [DRV_TEMPERATURE_CODES, "DRV_TEMPERATURE_CODES"],
    [DRV_TEMPERATURE_OFF, "DRV_TEMPERATURE_OFF"],
    [DRV_TEMPERATURE_NOT_STABILIZED, "DRV_TEMPERATURE_NOT_STABILIZED"],
    [DRV_TEMPERATURE_STABILIZED, "DRV_TEMPERATURE_STABILIZED"],
    [DRV_TEMPERATURE_NOT_REACHED, "DRV_TEMPERATURE_NOT_REACHED"],
    [DRV_TEMPERATURE_OUT_RANGE, "DRV_TEMPERATURE_OUT_RANGE"],
    [DRV_TEMPERATURE_NOT_SUPPORTED, "DRV_TEMPERATURE_NOT_SUPPORTED"],
    [DRV_TEMPERATURE_DRIFT, "DRV_TEMPERATURE_DRIFT"],
    [DRV_TEMP_CODES, "DRV_TEMP_CODES"],
    [DRV_TEMP_OFF, "DRV_TEMP_OFF"],
    [DRV_TEMP_NOT_STABILIZED, "DRV_TEMP_NOT_STABILIZED"],
    [DRV_TEMP_STABILIZED, "DRV_TEMP_STABILIZED"],
    [DRV_TEMP_NOT_REACHED, "DRV_TEMP_NOT_REACHED"],
    [DRV_TEMP_OUT_RANGE, "DRV_TEMP_OUT_RANGE"],
    [DRV_TEMP_NOT_SUPPORTED, "DRV_TEMP_NOT_SUPPORTED"],
    [DRV_TEMP_DRIFT, "DRV_TEMP_DRIFT"],
    [DRV_GENERAL_ERRORS, "DRV_GENERAL_ERRORS"],
    [DRV_INVALID_AUX, "DRV_INVALID_AUX"],
    [DRV_COF_NOTLOADED, "DRV_COF_NOTLOADED"],
    [DRV_FPGAPROG, "DRV_FPGAPROG"],
    [DRV_FLEXERROR, "DRV_FLEXERROR"],
    [DRV_GPIBERROR, "DRV_GPIBERROR"],
    [DRV_EEPROMVERSIONERROR, "DRV_EEPROMVERSIONERROR"],
    [DRV_DATATYPE, "DRV_DATATYPE"],
    [DRV_DRIVER_ERRORS, "DRV_DRIVER_ERRORS"],
    [DRV_P1INVALID, "DRV_P1INVALID"],
    [DRV_P2INVALID, "DRV_P2INVALID"],
    [DRV_P3INVALID, "DRV_P3INVALID"],
    [DRV_P4INVALID, "DRV_P4INVALID"],
    [DRV_INIERROR, "DRV_INIERROR"],
    [DRV_COFERROR, "DRV_COFERROR"],
    [DRV_ACQUIRING, "DRV_ACQUIRING"],
    [DRV_IDLE, "DRV_IDLE"],
    [DRV_TEMPCYCLE, "DRV_TEMPCYCLE"],
    [DRV_NOT_INITIALIZED, "DRV_NOT_INITIALIZED"],
    [DRV_P5INVALID, "DRV_P5INVALID"],
    [DRV_P6INVALID, "DRV_P6INVALID"],
    [DRV_INVALID_MODE, "DRV_INVALID_MODE"],
    [DRV_INVALID_FILTER, "DRV_INVALID_FILTER"],
    [DRV_I2CERRORS, "DRV_I2CERRORS"],
    [DRV_I2CDEVNOTFOUND, "DRV_I2CDEVNOTFOUND"],
    [DRV_I2CTIMEOUT, "DRV_I2CTIMEOUT"],
    [DRV_P7INVALID, "DRV_P7INVALID"],
    [DRV_P8INVALID, "DRV_P8INVALID"],
    [DRV_P9INVALID, "DRV_P9INVALID"],
    [DRV_P10INVALID, "DRV_P10INVALID"],
    [DRV_P11INVALID, "DRV_P11INVALID"],
    [DRV_USBERROR, "DRV_USBERROR"],
    [DRV_IOCERROR, "DRV_IOCERROR"],
    [DRV_VRMVERSIONERROR, "DRV_VRMVERSIONERROR"],
    [DRV_GATESTEPERROR, "DRV_GATESTEPERROR"],
    [DRV_USB_INTERRUPT_ENDPOINT_ERROR, "DRV_USB_INTERRUPT_ENDPOINT_ERROR"],
    [DRV_RANDOM_TRACK_ERROR, "DRV_RANDOM_TRACK_ERROR"],
    [DRV_INVALID_TRIGGER_MODE, "DRV_INVALID_TRIGGER_MODE"],
    [DRV_LOAD_FIRMWARE_ERROR, "DRV_LOAD_FIRMWARE_ERROR"],
    [DRV_DIVIDE_BY_ZERO_ERROR, "DRV_DIVIDE_BY_ZERO_ERROR"],
    [DRV_INVALID_RINGEXPOSURES, "DRV_INVALID_RINGEXPOSURES"],
    [DRV_BINNING_ERROR, "DRV_BINNING_ERROR"],
    [DRV_INVALID_AMPLIFIER, "DRV_INVALID_AMPLIFIER"],
    [DRV_INVALID_COUNTCONVERT_MODE, "DRV_INVALID_COUNTCONVERT_MODE"],
    [DRV_USB_INTERRUPT_ENDPOINT_TIMEOUT, "DRV_USB_INTERRUPT_ENDPOINT_TIMEOUT"],
    [DRV_ERROR_NOCAMERA, "DRV_ERROR_NOCAMERA"],
    [DRV_NOT_SUPPORTED, "DRV_NOT_SUPPORTED"],
    [DRV_NOT_AVAILABLE, "DRV_NOT_AVAILABLE"],
    [DRV_ERROR_MAP, "DRV_ERROR_MAP"],
    [DRV_ERROR_UNMAP, "DRV_ERROR_UNMAP"],
    [DRV_ERROR_MDL, "DRV_ERROR_MDL"],
    [DRV_ERROR_UNMDL, "DRV_ERROR_UNMDL"],
    [DRV_ERROR_BUFFSIZE, "DRV_ERROR_BUFFSIZE"],
    [DRV_ERROR_NOHANDLE, "DRV_ERROR_NOHANDLE"],
    [DRV_GATING_NOT_AVAILABLE, "DRV_GATING_NOT_AVAILABLE"],
    [DRV_FPGA_VOLTAGE_ERROR, "DRV_FPGA_VOLTAGE_ERROR"],
    [DRV_OW_CMD_FAIL, "DRV_OW_CMD_FAIL"],
    [DRV_OWMEMORY_BAD_ADDR, "DRV_OWMEMORY_BAD_ADDR"],
    [DRV_OWCMD_NOT_AVAILABLE, "DRV_OWCMD_NOT_AVAILABLE"],
    [DRV_OW_NO_SLAVES, "DRV_OW_NO_SLAVES"],
    [DRV_OW_NOT_INITIALIZED, "DRV_OW_NOT_INITIALIZED"],
    [DRV_OW_ERROR_SLAVE_NUM, "DRV_OW_ERROR_SLAVE_NUM"],
    [DRV_MSTIMINGS_ERROR, "DRV_MSTIMINGS_ERROR"],
    [DRV_OA_NULL_ERROR, "DRV_OA_NULL_ERROR"],
    [DRV_OA_PARSE_DTD_ERROR, "DRV_OA_PARSE_DTD_ERROR"],
    [DRV_OA_DTD_VALIDATE_ERROR, "DRV_OA_DTD_VALIDATE_ERROR"],
    [DRV_OA_FILE_ACCESS_ERROR, "DRV_OA_FILE_ACCESS_ERROR"],
    [DRV_OA_FILE_DOES_NOT_EXIST, "DRV_OA_FILE_DOES_NOT_EXIST"],
    [DRV_OA_XML_INVALID_OR_NOT_FOUND_ERROR, "DRV_OA_XML_INVALID_OR_NOT_FOUND_ERROR"],
    [DRV_OA_PRESET_FILE_NOT_LOADED, "DRV_OA_PRESET_FILE_NOT_LOADED"],
    [DRV_OA_USER_FILE_NOT_LOADED, "DRV_OA_USER_FILE_NOT_LOADED"],
    [DRV_OA_PRESET_AND_USER_FILE_NOT_LOADED, "DRV_OA_PRESET_AND_USER_FILE_NOT_LOADED"],
    [DRV_OA_INVALID_FILE, "DRV_OA_INVALID_FILE"],
    [DRV_OA_FILE_HAS_BEEN_MODIFIED, "DRV_OA_FILE_HAS_BEEN_MODIFIED"],
    [DRV_OA_BUFFER_FULL, "DRV_OA_BUFFER_FULL"],
    [DRV_OA_INVALID_STRING_LENGTH, "DRV_OA_INVALID_STRING_LENGTH"],
    [DRV_OA_INVALID_CHARS_IN_NAME, "DRV_OA_INVALID_CHARS_IN_NAME"],
    [DRV_OA_INVALID_NAMING, "DRV_OA_INVALID_NAMING"],
    [DRV_OA_GET_CAMERA_ERROR, "DRV_OA_GET_CAMERA_ERROR"],
    [DRV_OA_MODE_ALREADY_EXISTS, "DRV_OA_MODE_ALREADY_EXISTS"],
    [DRV_OA_STRINGS_NOT_EQUAL, "DRV_OA_STRINGS_NOT_EQUAL"],
    [DRV_OA_NO_USER_DATA, "DRV_OA_NO_USER_DATA"],
    [DRV_OA_VALUE_NOT_SUPPORTED, "DRV_OA_VALUE_NOT_SUPPORTED"],
    [DRV_OA_MODE_DOES_NOT_EXIST, "DRV_OA_MODE_DOES_NOT_EXIST"],
    [DRV_OA_CAMERA_NOT_SUPPORTED, "DRV_OA_CAMERA_NOT_SUPPORTED"],
    [DRV_OA_FAILED_TO_GET_MODE, "DRV_OA_FAILED_TO_GET_MODE"],
    [DRV_OA_CAMERA_NOT_AVAILABLE, "DRV_OA_CAMERA_NOT_AVAILABLE"],
    [DRV_PROCESSING_FAILED, "DRV_PROCESSING_FAILED"]
]

def code2msg(int code):
    for i in errorcodes:
        if (i[0] == code):
            return i[1]
    return "UNKNOWN_CODE"

def initialize():
    sta = andorsdk.Initialize(NULL)
    return code2msg(sta)

def getTemperature():
    cdef int * t = <int*> malloc(sizeof(int))
    sta = andorsdk.GetTemperature(t)
    cdef int re = dereference(t)
    return (code2msg(sta), re)

def getTemperatureRange():
    cdef int * t1 = <int*> malloc(sizeof(int))
    cdef int * t2 = <int*> malloc(sizeof(int))
    sta = andorsdk.GetTemperatureRange(t1, t2)
    cdef int re1 = dereference(t1)
    cdef int re2 = dereference(t2)
    return (code2msg(sta), re1, re2)

def setTemperature(int a):
    cdef int t = a
    sta = andorsdk.SetTemperature(t)
    return code2msg(sta)
    
def turnOffCooler():
    sta = andorsdk.CoolerOFF()
    return code2msg(sta)
    

def turnOnCooler():
    sta = andorsdk.CoolerON()
    return code2msg(sta)
    

def shutDown():
    sta = andorsdk.ShutDown()
    return code2msg(sta)

def setReadMode(mode=4):
    sta = andorsdk.SetReadMode(mode)
    return code2msg(sta)


def setExposureTime(time):
    sta = andorsdk.SetExposureTime(time)
    return code2msg(sta)

def setShutter(typ=0, mode=0, closingtime=0, openingtime=0):
    sta = andorsdk.SetShutter(typ, mode, closingtime, openingtime)
    return code2msg(sta)

def setAcquisitionMode(mode=1):
    sta = andorsdk.SetAcquisitionMode(mode)
    return code2msg(sta)

def setImage(hbin=2, vbin=2, hstart=1, hend=1024, vstart=1, vend=1024):
    sta = andorsdk.SetImage(hbin, vbin, hstart, hend, vstart,vend)
    return code2msg(sta)


def startAcquisition():
    sta = andorsdk.StartAcquisition()
    return code2msg(sta)


def getStatus():
    cdef int * t = <int*> malloc(sizeof(int))
    sta = andorsdk.GetStatus(t)
    cdef int re = dereference(t)
    return (code2msg(sta), code2msg(re))


def getImage(hbin=2, vbin=2, hstart=1, hend=1024, vstart=1, vend=1024):
    height = int((vend - vstart + 1)/vbin)
    width = int((hend - hstart + 1)/hbin)

    cdef at_u32 size = height*width
    cdef at_32 * t = <at_32*> malloc(sizeof(at_32)*size)
    
    sta = andorsdk.GetMostRecentImage(t, size)
    
    if (code2msg(sta) != "DRV_SUCCESS"):
        return (code2msg(sta), 0)

    re = []
    for i in range(0, height):
        row = []
        for j in range(0, width):
            row.append(t[i*width + j])
        re.append(row)
    
    re = np.array(re)
    re = np.flip(re, 0)

    return (code2msg(sta), re)

