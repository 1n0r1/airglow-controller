cimport andorsdk
from cython.operator import dereference
from libc.stdlib cimport malloc, free

cdef class Andorsdk:
    def __cinit__(self):
        sta = andorsdk.Initialize(NULL)
        print(sta)
    
    def getTemperature(self) -> int:
        cdef int * t = <int*> malloc(sizeof(int))
        sta = andorsdk.GetTemperature(t)
        print(sta)
        cdef int re = dereference(t)
        return re
        