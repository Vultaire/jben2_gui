# -*- coding: utf-8 -*-

from __future__ import absolute_import

from optparse import OptionParser
from jben.app import Application
import gettext
gettext.install("jben")

def parse_args():
    op = OptionParser()
    op.set_defaults(interface="gtk")
    op.add_option("-i", "--interface",
                  help=_("Select interface: gtk, console (default: %default)"))
    return op.parse_args()

def main():
    (options, args) = parse_args()
    app = Application(interface=options.interface)
    app.run()

if __name__ == "__main__":
    main()
