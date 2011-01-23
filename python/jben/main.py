# -*- coding: utf-8 -*-

from __future__ import absolute_import

from optparse import OptionParser
from jben.app import Application
import gettext, locale, os

def init_windows_locale():
    """Sets expected environment variables for Windows.

    If LANG is already specified, this will have no effect.

    """
    if "LANG" not in os.environ:
        def_locale, def_encoding = locale.getdefaultlocale()
        os.environ["LANG"] = def_locale

def init_gettext():
    """Initializes gettext globally."""
    # This function may be replaced later to support dynamic language switching.
    gettext.install("jben", localedir="locale", unicode=True)

def parse_args():
    op = OptionParser()
    op.set_defaults(interface="gtk")
    op.add_option("-i", "--interface",
                  help=_("Select interface: gtk, console (default: %default)"))
    return op.parse_args()

def main():
    if os.name == "nt":
        init_windows_locale()
    init_gettext()
    (options, args) = parse_args()
    app = Application(interface=options.interface)
    app.run()

if __name__ == "__main__":
    main()
