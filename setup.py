from setuptools import setup
from Cython.Build import cythonize
from Cython.Compiler import Options
from Cython.Distutils import build_ext
Options.embed = "main"

setup(
    name='Hello world app',
    cmdclass={'build_ext':build_ext},
    ext_modules=cythonize(("container.py", "Generation/generation.py", "Solving/solving.py", "main.py")),
    zip_safe=False,
)

