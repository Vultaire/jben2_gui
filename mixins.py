#!/usr/bin/env python
# -*- coding: utf-8 -*-

import preferences

class StoredSize:

    def __init__(self, param=None, width=-1, height=-1):
        self.param_name = param
        pref = None
        if param:
            pref = preferences.options.get(param)
        if pref:
            width, height = [int(v) for v in pref.split("#", 1)]
        self.set_default_size(width, height)

    def destroy(self):
        print "DEBUG: ", self.get_size()
        preferences.options[self.param_name] = "x".join(
            [str(v) for v in self.get_size()])
        print "DEBUG: ", preferences.options[self.param_name]
