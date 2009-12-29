#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module used for holding "global" module references.

Some objects are very widely used in J-Ben (the JBen object, the
Preferences object).  Including these explicitly all the time is a bit
of a typing contest, so code which requires info from a "singleton"
object such as these can use this module to fetch the reference.

"""

jben = None
prefs = None
