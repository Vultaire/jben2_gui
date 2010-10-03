J-Ben: a Japanese study program
Copyright 2007, 2008, 2009, 2010 by Paul Goins
Released under the GNU General Public License (GPL), version 2 or above

This program should be considered "alpha" status and is not intended
for everyday use.


For installation, see INSTALL.txt.
For license information, see COPYING.txt.


Summary of current status:

  - The kanji and word dictionaries work at a basic level, but are by
    no means fast.  They are pending cleanup if not a rewrite.  (I
    knew much less about Python at the time I wrote them than I do
    now.)

  - Improvement over J-Ben 1.2.3: Startup time is nearly instantaneous
    since dictionary data is not loaded until one of the dictionaries
    is queried.

  - The preferences menu, although present, does not actually do
    anything meaningful yet.

  - Most advanced features in the program are not yet present.  (Study
    lists, kanji practice mode, character/word cross referencing.

  - The program can be hooked into jben_kpengine for handwriting
    recognition support.  However, the path is currently hardcoded.
    This is a temporary situation; I plan on making a Python module
    equivalent to that code in the future.


As always, feedback and patches are welcome.

- Paul
