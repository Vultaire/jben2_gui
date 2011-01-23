#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.67])
AC_INIT([J-Ben 2 BETA],
        [1.9.5],
        [general at vultaire dot net],
        [jben],
        [http://jben.vultaire.net/])
AM_INIT_AUTOMAKE([foreign])
AC_CONFIG_SRCDIR([c/kpengine/jstroke.h])
AC_CONFIG_HEADERS([config.h])

# Checks for programs.
AC_PROG_CC
AM_PROG_CC_C_O

# Checks for libraries.

# Checks for header files.
AC_CHECK_HEADERS([stdlib.h string.h])
# Others: stdio.h, ctype.h, windows.h (windows only)

# Checks for typedefs, structures, and compiler characteristics.
AC_HEADER_STDBOOL

# Checks for library functions.
AC_FUNC_MALLOC
AC_FUNC_REALLOC
AC_CHECK_FUNCS([strdup strtol])

# Check for gettext
AM_GNU_GETTEXT([external])
AM_GNU_GETTEXT_VERSION([0.17])

AC_CONFIG_FILES([Makefile po/Makefile.in
                 c/Makefile
                 c/kpengine/Makefile
                 data/Makefile
                 python/Makefile
                 python/jben/configure.py])
AC_OUTPUT
