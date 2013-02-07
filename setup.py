# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import sys, os

__version__ = '0.1'

setup(name='whois',
      version=__version__,
      description="",
      long_description="",
      classifiers=[], 
      keywords='whois',
      author='Larry Kim',
      author_email='admin@relip.org',
      url='http://github.com/relip/python-whois',
      license='MIT',
	package_dir={},
      packages=['whois'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
)
