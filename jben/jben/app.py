# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
from jben.preferences import Preferences
from jben.dict import DictManager
from jben import global_refs


class Application(object):

    def __init__(self, interface):
        mod = __import__("jben.interface", globals(), locals(), [interface], 0)
        if interface not in dir(mod):
            raise Exception(_("Interface %s does not exist.") % interface)
        self.interface = getattr(mod, interface).Interface(self)
        self.prefs = Preferences()
        self.dictmgr = DictManager(self)
        global_refs.app = self

    def run(self):
        result = self.interface.run()
        self.prefs.save()
        return result

    def get_data_dir(self):
        """Configures the "data directory" for J-Ben.

        The installed directory will be used if permissions allow.
        Otherwise, the user's home directory will be used.

        """
        dirs_d = {
            "nt": [".."],
            "posix": ["/usr/local/share/jben",
                      "/usr/share/jben"],
            }
        dirs = dirs_d[os.name]
        dirs.append(self.get_home_dir())

        for d in dirs:
            if os.path.exists(d) and os.access(d, os.W_OK):
                return d
        raise Exception(_("Could not find writable data directory"))

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
