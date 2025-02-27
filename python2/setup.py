from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize(
        'CRISPResso2Align.pyx',
        language_level=2,
    ),
    include_dirs=[numpy.get_include()],
)
