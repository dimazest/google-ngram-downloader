import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--recreate']
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


dirname = os.path.dirname(__file__)

long_description = (
    open(os.path.join(dirname, 'README.rst')).read() + '\n' +
    open(os.path.join(dirname, 'CHANGES.rst')).read()
)


setup(
    name='google-ngram-downloader',
    version='3.0.1',
    description='The streaming access to the Google ngram data.',
    long_description=long_description,
    # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    keywords='',
    author='Dmitrijs Milajevs',
    author_email='dimazest@gmail.com',
    url='https://github.com/dimazest/google-ngram-downloader',
    license='MIT license',
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
    tests_require=['tox'],
    cmdclass={'test': Tox},
)
