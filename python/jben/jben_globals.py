#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: jben_global.py
# Author: Paul Goins
# Created on: 25 Nov 2008

from __future__ import absolute_import

import os
import gettext
gettext.install("jben")

VERSION_STR = "1.9.2"
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
COPYRIGHT_DATE = _("2007, 2008, 2009, 2010")
"""Copyright date."""
