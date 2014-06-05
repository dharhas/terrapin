import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)
# this sets __version__
info = {}
execfile(os.path.join('terrapin', 'version.py'), info)


with open('README.rst') as f:
    # use README for long description but don't include the link to travis-ci;
    # it seems a bit out of place on pypi since it applies to the development
    # version
    long_description = ''.join([
        line for line in f.readlines()
        if 'travis-ci' not in line])


setup(
    name='terrapin',
    version=info['__version__'],
    license='BSD',
    author='Dharhas Pothina',
    author_email='dharhas@gmail.com',
    description='numpy aware Digital Elevation Model (DEM) analysis tools',
    long_description=long_description,
    url='https://github.com/dharhas/terrapin',
    keywords='dem raster d8 flow direction dinfinity',
    packages=find_packages(),
    platforms='any',
    install_requires=[
        'numpy>=1.4.0',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    tests_require=[
        'pytest>=2.3.2',
    ],
    cmdclass={'test': PyTest},
)