from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    ext_modules=cythonize(
        'python3/CRISPResso2Align.pyx',
        build_dir='python3',
        language_level=3,
    ),
    include_dirs=[numpy.get_include()],
)
