#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from jben import jben_global

setup(name='jben',
      version=jben_global.VERSION_STR,
      description='J-Ben parsing library',
      author=jben_global.AUTHOR_NAME,
      author_email='general@vultaire.net',
      url='http://jben.vultaire.net/',
      packages=['jben', 'jben.gui'],
      package_data={'jben': ['images/*.xpm']},
      requires=['jbparse'],
      classifiers=[
          'Environment :: Win32 (MS Windows)',
          'Environment :: X11 Applications :: GTK',
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Natural Language :: English',
          'Operating System :: Microsoft :: Windows :: Windows NT/2000',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Education'
          ]
      )
