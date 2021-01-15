from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize(
        'python2/CRISPResso2Align.pyx',
        build_dir='python2',
        language_level=2,
    ),
    include_dirs=[numpy.get_include()],
)
