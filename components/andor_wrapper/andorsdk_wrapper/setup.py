from setuptools import Extension, setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize([
        Extension("andorsdk", ["andorsdk.pyx"],
                    libraries=["andor"])
        
        ])
)