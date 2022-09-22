
cdef extern from "./include/atmcdLXd.h":
    unsigned int Initialize(char * dir)
    unsigned int GetTemperature(int * temperature)
