#!/usr/bin/env python
"""J-Ben launch script"""
from jben import main

# This is a workaround for py2exe...
from xml.etree import ElementTree as _
del _

main.main()
