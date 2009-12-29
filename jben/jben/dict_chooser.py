# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys, os
from jben.preferences import Preferences
from jben.console import y_or_n
from jben.dict_downloader import download_dict


class DictEntry(object):

    """Class for dictionary preference entries."""

    def __init__(self, filename, encoding=None):
        self.filename = filename
        if encoding is not None:
            self.encoding = encoding
        else:
            self._auto_encode()

    def _auto_encode(self):
        """Automatic encoding selection function."""
        # Automatic encoding selection based on file name
        fn = self.filename.split(".")[0].lower()
        if any([fn.find(s) == 0 for s in ["jmdict", "kanjidic2"]]):
            self.encoding = "utf-8"
        elif any([fn.find(s) == 0 for s in ["edict", "kanjidic", "kanjd212"]]):
            self.encoding = "euc-jp"
        else:
            # Default encoding...  I need to check what other
            # EDICT-style dictionaries are using nowadays.  My
            # strong preference is to do everything as UTF-8.
            self.encoding = "utf-8"


def set_dicts(option_key, d_entries):

    """Updates preferences with selected dictionary objects.

    Given a preference key (dict.kanji for example) and a list of
    dictionary entry objects, create appropriate keys.

    For example, with dict.kanji as the key and a list of [kanjidic,
    kanjd212] entry objects, the following keys may be created:

    dict.kanji.1.file: kanjidic.gz
    dict.kanji.1.encoding: euc-jp
    dict.kanji.2.file: kanjd212.gz
    dict.kanji.2.encoding: euc-jp

    On update, any existing entries which start with the specified
    option key will be dropped.

    """

    # Clear previous entries
    prefs = refs.prefs
    keys = [k for k in prefs if k.find(option_key) == 0]
    keys.sort()
    for k in keys:
        #print "%s: %s" % (k, str(prefs[k]))
        del prefs[k]
    # Store new entries
    for i, de in enumerate(d_entries):
        i += 1
        basekey = "%s.%d" % (option_key, i)
        filekey = "%s.filename" % basekey
        encodekey = "%s.encoding" % basekey
        prefs[filekey] = de.filename
        prefs[encodekey] = de.encoding

def set_word_dicts(dicts):
    set_dicts("dict.word", dicts)

def set_kanji_dicts(dicts):
    set_dicts("dict.kanji", dicts)



def console_chooser():
    """Select dictionaries from the console."""

    word_dicts = (("EDICT:    172143 entries.  Small, fast, commonly used by "
                   "other programs.", "edict.gz"),
                  #("EDICT2:   144541 entries.  Newer, more compact version of "
                  # "EDICT.", "edict2.gz"),
                  ("JMdict:   144727 entries.  Multiple language glosses.  "
                   "Big, slow, detailed.", "jmdict.gz"),
                  ("JMdict_e: English-only version of JMdict.", "jmdict_e.gz"))
    kanji_dicts = (("KANJIDIC:  Standard kanji dictionary.  6355 entries.  "
                    "Small, very fast", "kanjidic.gz"),
                   ("KANJD212:  Extension to KANJIDIC.  5801 entries.  "
                    "Not commonly needed.", "kanjd212.gz"),
                   ("KANJIDIC2: Newer XML-based dictionary.  13108 entries.  "
                    "A little slow.", "kanjidic2.xml.gz"))

    def run_chooser(dicts, default):
        # Print dictionary descriptions
        for i, (desc, fname) in enumerate(dicts):
            i += 1
            print "%d. %s" % (i, desc)
        print

        print ("Please choose which dictionaries to use.  More than one "
               "can be specified if you put spaces between them.")
        print
        while True:
            # Get selection
            default = [1]
            sys.stdout.write("Your choice [Default: %s]: "
                             % " ".join(map(str, default)))
            try:
                choices = map(int, sys.stdin.readline().strip().split())
            except:
                continue
            if len(choices) == 0:
                choices = default
            if all([i in range(1, 1+len(dicts)) for i in choices]):
                break

        return [DictEntry(dicts[i-1][1]) for i in choices]

    # Choose word dicts
    print "J-Ben supports the following word dictionary files:"
    print
    dicts = run_chooser(word_dicts, [1])
    set_word_dicts(dicts)

    # Choose kanji dicts
    print "J-Ben supports the following kanji dictionary files:"
    print
    dicts = run_chooser(kanji_dicts, [1])
    set_kanji_dicts(dicts)

    # ...confirm changes?
    print "You've chosen the following settings:"
    print
    prefs = refs.prefs
    word_keys = [k for k in prefs if k.find("dict.word") == 0]
    kanji_keys = [k for k in prefs if k.find("dict.kanji") == 0]
    keys = word_keys + kanji_keys
    keys.sort()
    for k in keys:
        print "\t%s: %s" % (k, prefs[k])
    print
    choice = y_or_n("Is this okay?", "n")

    if choice != 'y':
        return
    prefs.save()

    # Check existence of dictionary files.  If some are not present,
    # offer to download.
    dpath = prefs.get_dict_path()
    fn_keys = [k for k in keys if "filename" in k]
    files = [prefs[k] for k in fn_keys]
    fnames = [os.path.join(dpath, fname) for fname in files]
    needed_files = [os.path.split(fname)[-1] for fname in fnames
                    if not os.path.exists(fname)]
    if needed_files:
        needed_files.sort()
        print
        print "The following dictionary files could not be found:"
        print
        for i, f in enumerate(needed_files):
            i += 1
            print "%d. %s" % (i, f)
        print
        choice = y_or_n("Do you wish to download them?", "y")

        if choice == 'y':
            for f in needed_files:
                download_dict(f)

if __name__ == "__main__":
    console_chooser()
