import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = 'test'
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


dirname = os.path.dirname(__file__)


def read_file(f_name):
    with open(f_name) as f:
        return f.read()


long_description = '\n'.join(
    [
        read_file(os.path.join(dirname, 'README.rst')),
        read_file(os.path.join(dirname, 'CHANGES.rst')),
    ]
)


setup(
    name='google-ngram-downloader',
    version='4.1.0',
    description='The streaming access to the Google ngram data.',
    long_description=long_description,
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Utilities',
        'Topic :: Text Processing :: Linguistic',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    keywords='',
    author='Dmitrijs Milajevs',
    author_email='dimazest@gmail.com',
    url='https://github.com/dimazest/google-ngram-downloader',
    license='MIT License',
    packages=find_packages(exclude=['ez_setup', 'examples', 'test']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'opster',
        'py',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'google-ngram-downloader = google_ngram_downloader.__main__:dispatcher.dispatch',
        ],
    },
    tests_require=[
        'pytest>=2.4.2',
    ],
    cmdclass={'test': PyTest},
)
