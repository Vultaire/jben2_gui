# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
from jben.preferences import Preferences
from jben.dict import DictManager
from jben import global_refs


class Application(object):

    def __init__(self, interface):
        if interface == "gtk":
            from jben.interface import gtk
            self.interface = gtk.Interface(self)
        elif interface == "console":
            from jben.interface import console
            self.interface = console.Interface(self)
        else:
            raise ValueError(_("Interface not supported"), interface)

        self.prefs = Preferences(self)
        self.dictmgr = DictManager(self)
        global_refs.app = self

    def run(self):
        result = self.interface.run()
        self.prefs.save()
        return result

    def get_home_dir(self):
        env_d = {
            "nt": "APPDATA",
            "posix": "HOME",
            }
        env = env_d[os.name]
        home = os.getenv(env)
        assert home, _("Could not get home directory from environment.")
        return home

    def get_settings_dir(self):
        dir_d = {
            "nt": "J-Ben Settings",
            "posix": ".jben.d",
            }
        path = os.path.join(self.get_home_dir(), dir_d[os.name])
        return path
