# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import sys, os

__version__ = '0.1'

setup(name='whois',
	version=__version__,
	description="The Whois client, which is developed in Python language, retrieves domain information from the server.",
	classifiers=[
		"License :: OSI Approved :: MIT License",
		"Operating System :: POSIX",
		"Environment :: Console",
		"Programming Language :: Python",
		"Topic :: Internet",
		"Topic :: Software Development :: Libraries :: Python Modules",
	], 
	keywords='whois',
	author='Larry Kim',
	author_email='admin@relip.org',
	url='http://github.com/relip/python-whois',
	license='MIT',
	packages=['whois'],
)
