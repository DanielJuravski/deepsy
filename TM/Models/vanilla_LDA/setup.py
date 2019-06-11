from distutils.core import setup
from Cython.Build import cythonize
import numpy

setup(
    name='TM sampler',
    ext_modules=cythonize(module_list="LDAGibbs.pyx",
                          compiler_directives={'language_level': "3"}),
    include_dirs=[numpy.get_include()]
)
