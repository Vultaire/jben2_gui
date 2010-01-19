# -*- coding: utf-8 -*-

from __future__ import absolute_import


from jben.preferences import Preferences
from jben.dict import DictManager
from jben import global_refs


class Application(object):

    def __init__(self, interface):
        mod = __import__("jben.interface", globals(), locals(), [interface], 0)
        if interface not in dir(mod):
            raise Exception("Interface %s does not exist." % interface)
        self.interface = getattr(mod, interface).Interface(self)
        global_refs.prefs = Preferences()
        global_refs.dictmgr = DictManager()

    def run(self):
        return self.interface.run()
