#!/usr/bin/env python
#
# Source:
# http://blog.wearpants.org/integrating-coverage-and-unittest-discovery
#
# Run via::
#
#   python -m coverage run unittest_main.py [args]
#
# What was done: Python/Lib/unittest/__main__.py was copied VERBATIM
# here.  This means that running this script via coverage effectively
# provides a wrapper around "python -m unittest".  Pass arguments
# afterwards like normal.
#
# Unit test coverage with automatic discovery::
#
#   python -m coverage run unittest_main.py discover

"""Main entry point"""

import sys
if sys.argv[0].endswith("__main__.py"):
    sys.argv[0] = "python -m unittest"

__unittest = True

from unittest.main import main, TestProgram, USAGE_AS_MAIN
TestProgram.USAGE = USAGE_AS_MAIN

main(module=None)
