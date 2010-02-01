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
        self.prefs = Preferences()
        self.dictmgr = DictManager(self)
        global_refs.app = self

    def run(self):
        result = self.interface.run()
        self.prefs.save()
        return result
