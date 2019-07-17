from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize("*.pyx"),
    include_dirs=['/anaconda2/lib/python2.7/site-packages/numpy/core/include/']
)
