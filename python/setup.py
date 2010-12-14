#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from jben import configure


# Py2exe include (Windows only)
try:
    import py2exe
except ImportError:
    # Py2exe is not *required*...
    pass


setup(name='jben',
      version=configure.PACKAGE_VERSION,
      description='J-Ben: A Japanese study program (alpha)',
      author=jben_globals.AUTHOR_NAME,
      author_email='general@vultaire.net',
      url='http://jben.vultaire.net/',
      packages=[
        'jben',
        'jben.test',
        'jben.interface',
        'jben.interface.console',
        'jben.interface.gtk',
        'jben.interface.gtk.dialog',
        'jben.interface.gtk.dialog.preferences',
        'jben.interface.gtk.widget',
        'jben.interface.gtk.window',
        ],
      package_data={'jben': ['data/images/*.xpm']},
      scripts=["scripts/jben.py"],
      install_requires=['jblite', 'PyGTK'],
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
          ],

      # for py2exe
      windows = [{"script": "scripts/jben.py"}],
      data_files=[("data/images",
                   ["data/images/jben.xpm", "data/images/jben_16.xpm",
                    "data/images/jben_32.xpm", "data/images/jben_48.xpm"])],
      options = {
        "py2exe": {
            "packages": "encodings",
            "includes": "cairo, pango, pangocairo, atk, gobject, gio",
            }
        }
      )
