# -*- coding: utf-8 -*-
from setuptools import setup
from postman import __version__

setup(
    name='postman',
    version=__version__,
    author='Juan Diego Godoy Robles',
    author_email='klashxx@gmail.com',
    description='Just another mail sender',
    license='MIT',
    keywords='mail sender',
    url='https://klashxx.github.io/',
    py_modules=['postman'],
    entry_points={
        'console_scripts': [
            'postman = postman:cli',
        ]
    },
    long_description=open('README.md').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'License :: OSI Approved :: MIT License',
    ],
    tests_require=['pytest']
)
