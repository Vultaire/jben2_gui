Due to issues between gettext, Windows, and MinGW, J-Ben currently
does not rely on gettext suport via the Autotools.  Strings are
manually extracted, translated and compiled.

----------------------------------------------------------------------

Logic for creating and updating gettext-compatible message catalogs is
contained within the update_po_files.sh shell script.  It has been
tested and works with recent versions of MinGW/Msys (2010-12-23).

