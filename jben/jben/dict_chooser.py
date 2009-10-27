# -*- coding: utf-8 -*-

from __future__ import absolute_import

import jben.preferences as p

dicts = (("EDICT (Small, fast)"),
         #("EDICT2 (Smaller, fast) Recommended)"),
         ("JMdict (Huge, slow, detailed) (full)"),
         ("JMdict_e (Huge, slow, detailed) (English only)"),
         ("KANJIDIC (Small, very fast)"),
         #("KANJD212"),
         ("KANJIDIC2 (Large, a little slow)"))


# To store:
# 1. Chain of word dictionaries
# 2. Chain of kanji dictionaries
#
# In both cases, searches proceed through the chain until results are
# returned by one of them.  In most cases, only the first dictionary
# will ever be examined.

def set_dicts(dicts, option_key):
    keylen = len(option_key)
    if dicts and (type(dicts) == dict):
        # Clear previous entries
        keys = p.options.keys()
        for key in [k for k in keys if k[:keylen] == option_key]:
            del p.options[key]
        # Store new ones
        for i, d in enumerate(dicts.iteritems()):
            p.options["%s.%d" % (option_key, i)] = d

def set_word_dicts(dicts):
    set_dicts(dicts, "dict.word")

def set_kanji_dicts(dicts):
    set_dicts(dicts, "dict.kanji")

def console_chooser():
    """Select dictionaries from the console."""
    pass

if __name__ == "__main__":
    p.load()
    console_chooser()
