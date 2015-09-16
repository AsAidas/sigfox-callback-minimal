__author__ = 'hbuyse'

import os
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import sys

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

if sys.version_info < (3, 0):
    install_requires = [
        "PyMySQL==0.6.6",
        "requests==2.7.0"

    ]
else:
    install_requires = [
    ]

dev_requires = [
]

tests_require = [
    'pytest>=2.5.1',
]

# MODIFY FROM HERE
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

# TODO: move manage.py into forge_app and introduce it as an entry point of the virtual environment
setup(
    name='tim-callback-minimal',
    version='1.1.0',
    packages=find_packages('.'),
    include_package_data=True,
    license='',  # example license
    description='Sigfox callback minimal HTTP server for TIM Project',
    long_description=README,
    url='https://bitbucket.org/timhelmet/tim-callback-minimal',
    author='hbuyse',
    author_email='hbuyse@astek.fr',
    extras_require={
        'tests': tests_require,
        'dev': dev_requires,
    },
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    classifiers=[
        'Environment :: Network Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2'
    ],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'tim-astek = tim_callback_minimal.main:main',
        ]
    }
)
