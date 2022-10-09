cimport lasershutter

from cython.operator import dereference
from libc.stdlib cimport malloc, free



cdef class Lasershutter:
    
    def __cinit__(self):
        pass
    