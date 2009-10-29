J-Ben: a Japanese study program
Copyright 2007, 2008, 2009 by Paul Goins
Released under the GNU General Public License (GPL), version 2 or above

This program should be considered Pre-Alpha, as it does not yet
function even at a basic level as it is intended.  It is little more
than a GUI shell at this point.

Installation:

        python setup.py install

Running the program:

        python -m jben.jben

At this point, a basic PyGTK GUI is operational and some user settings
will be saved in ~/.jben (POSIX) or "%APPDATA%\J-Ben Settings"
(Windows).  However, dictionaries are not yet linked into the program,
so it is not usable for practical purposes.

The program can be hooked into jben_kpengine.exe, but the path is
currently hardcoded.  This is a temporary situation; I plan on making
a Python module equivalent to that code.  However, people interesting
in testing things can do so; handwriting recognition does work if
J-Ben can find jben_kpengine.

Feedback and patches are welcome.

- Paul
