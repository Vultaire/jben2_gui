#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.67])
AC_INIT([J-Ben], [1.9.2], [general at vultaire dot net])
AM_INIT_AUTOMAKE([foreign])
AC_CONFIG_SRCDIR([kpengine/jstroke.h])
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

AC_CONFIG_FILES([Makefile
                 kpengine/Makefile
                 jben/configure.py])
AC_OUTPUT
