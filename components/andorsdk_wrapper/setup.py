from setuptools import Extension, setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize([
        Extension("errorcodestable", ["errorcodestable.pyx"]),
        Extension("andorsdk", ["andorsdk.pyx"],
                    libraries=["andor"])
        
        ])
)