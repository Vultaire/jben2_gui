# -*- coding: utf-8 -*-

from __future__ import absolute_import


from jben.preferences import Preferences, DictEntry
from jben import global_refs
from jbparse import kanjidic, kanjidic2, edict, edict2, jmdict


class DictManager(object):

    """Dictionary manager class."""

    def __init__(self):
        self.kdictcache = {}
        self.wdictcache = {}
        self.kdicts = None
        self.wdicts = None

    def get_dicts(self, key):
        prefs = global_refs.prefs
        dict_keys = (k for k in prefs if k.startswith("%s." % key))
        # Indices are the 3rd element in the keys... grab all
        # unique indices
        indices = sorted(list(
            set([int(k.split(".")[2]) for k in dict_keys])))
        dictentry_d = {}
        for i in indices:
            de = DictEntry(
                prefs.get("%s.%d.filename" % (key, i)),
                prefs.get("%s.%d.encoding" % (key, i)))
            if de.filename:
                dictentry_d[i] = de
        dictfiles = (dictentry_d[i].filename
                     for i in indices if i in dictentry_d)
        dicts = [globals()[dictentry_d[i].format]
                 .Parser(dictentry_d[i].filename)
                 for i in indices if i in dictentry_d]
        return dicts

    def get_kanji_dict(self):
        # In the future we may support dict iteration.  For now let's
        # keep it simple!
        if not self.kdicts:
            self.kdicts = self.get_dicts("dictfile.kanji")
        return self.kdicts[0] if self.kdicts else None

    def get_word_dict(self):
        if not self.wdicts:
            self.wdicts = self.get_dicts("dictfile.word")
        return self.wdicts[0] if self.wdicts else None

    def reset_cache(self):
        self.kdictcache.clear()
        self.wdictcache.clear()
        self.kdicts = None
        self.wdicts = None
