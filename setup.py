#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from jben import jben_globals

setup(name='jben',
      version=jben_globals.VERSION_STR,
      description='J-Ben: A Japanese study program (alpha)',
      author=jben_globals.AUTHOR_NAME,
      author_email='general@vultaire.net',
      url='http://jben.vultaire.net/',
      packages=[
        'jben',
        'jben.interface',
        'jben.interface.console',
        'jben.interface.gtk',
        'jben.interface.gtk.dialog',
        'jben.interface.gtk.dialog.preferences',
        'jben.interface.gtk.widget',
        'jben.interface.gtk.window',
        ],
      package_data={'jben': ['images/*.xpm']},
      install_requires=['jbparse'],
      classifiers=[
          'Environment :: Win32 (MS Windows)',
          'Environment :: X11 Applications :: GTK',
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Natural Language :: English',
          'Operating System :: Microsoft :: Windows :: Windows NT/2000',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Education'
          ]
      )
