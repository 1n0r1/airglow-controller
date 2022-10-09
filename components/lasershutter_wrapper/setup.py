from setuptools import Extension, setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize([
        Extension("lasershutter", ["lasershutter.pyx"],
                    libraries=["PiUsb"],
                    library_dirs=["./x64"],
                    runtime_library_dirs=["./x64"]
                    )
        
        ])
)