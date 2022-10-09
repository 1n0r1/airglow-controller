
cdef extern from "./PiUsb.h":
    void * __stdcall piConnectShutter(int * ErrorNumber, int SerialNum)
    void __stdcall piDisconnectShutter(void * devicePtr)
    int __stdcall piSetShutterState(int ShutterState, void * devicePtr)
    int __stdcall piGetShutterState(int * CurrentShutterState, void * devicePtr)
    
