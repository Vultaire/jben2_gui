#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: jben_global.py
# Author: Paul Goins
# Created on: 25 Nov 2008

import os

VERSION_STR = "1.99"
"""This is the current version of J-Ben."""

# These were "constants" under the C++ interface.
# However, since J-Ben has an alternate Japanese name (Ｊ勉),
# and since my name can be written in katakana, or the copyright
# date written in other numbering systems (heisei-based, etc.),
# I'm now using gettext on these "constants".
PROGRAM_NAME = _("J-Ben/python")
"""The name of this edition of J-Ben."""
AUTHOR_NAME = _("Paul Goins")
"""The name of the author."""
COPYRIGHT_DATE = _("2007, 2008")
"""Copyright date."""


JB_DATADIR = None
"""
This represents the default data directory for J-Ben.  For UNIX-type systems,
this typically is "/usr/local/share/jben" or "/usr/share/jben".  For Windows
systems, it should be "..".  (Note the /; J-Ben will convert /'s to \'s as
necessary.)

If JB_DATADIR is None, then J-Ben will try to search all these locations for
the data folder.  This can be overridden by specifying a specific value here.
"""

if JB_DATADIR is None:
    if os.name == "nt":
        JB_DATADIR = ".."
    else:
        if os.path.isdir("/usr/local/share/jben"):
            JB_DATADIR = "/usr/local/share/jben"
        elif os.path.isdir("/usr/share/jben"):
            JB_DATADIR = "/usr/share/jben"
        else:
            JB_DATADIR = ".." # Fallback; this may be used on future Linux-based
            #                   mobile installs.
        pass

if os.name == "nt":
    CFG_FOLDER = "J-Ben Settings"
    HOME_ENV = "APPDATA"
else:
    CFG_FOLDER = ".jben.d"
    HOME_ENV = "HOME"
