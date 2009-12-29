#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: preferences.py
# Author: Paul Goins
# Created on: 20 December 2008

# NOTE: This module contains code written by other people but
# available (to the best of my knowledge) under a compatible license.
# Such code is clearly marked.

from __future__ import absolute_import

import sys, os, re
from jben import jben_globals

def make_alnum_tuple(str):
    # From Chris Hulan's alphanum.py chunkify function, available at
    # http://www.davekoelle.com/alphanum.html.
    print "==========="
    print str
    print "==========="
    chunks = re.findall("(\d+|\D+)", str)
    chunks = [re.match('\d',x) and int(x) or x for x in chunks]
    return chunks


class Preferences(dict):

    CURRENT_CONFIG_VERSION = make_alnum_tuple("2.0")

    def __init__(self):
        dict.__init__(self)
        self.set_default_prefs()
        self.load()
        if self.is_outdated():
            preferences.upgrade_config_file()
        # This variable will be set to the contents of
        # prefs["config_save_target"] when a config file is loaded,
        # in order to track runtime changes.
        self.original_save_target = self["config_save_target"]

    def is_outdated(self):
        version = make_alnum_tuple(self.get('config_version', "0"))
        return version < Preferences.CURRENT_CONFIG_VERSION

    def load(self, filename=None):
        """Load preferences from a config file.

        If filename is None (default), then J-Ben will search for a config
        file in the program's parent directory (important for self-contained
        "mobile" installs), followed by the user's home directory.

        """
        global original_save_target
        loaded = False

        if filename:
            try:
                f = open(filename)
                print "Reading from file:", filename
                lines = f.readlines()
                f.close()

                for line in lines:
                    line = line.strip()
                    # Treat # and ; as comment markers, and ignore empty lines.
                    if len(line) == 0 or line[0] == "#" or line[0] == ";":
                        continue

                    try:
                        k, v = re.split("[ \t=:]+", line, 1)
                        if k and v:
                            v2 = v.lower().strip()
                            if v2 in ("true", "false"):
                                self[k] = (v2 == "true")
                            else:
                                self[k] = v
                    except ValueError:
                        print _("Warning: unable to split line: %s" % line)
                self.original_save_target = self["config_save_target"]
            except IOError, e:
                if e.args[0] == 2:  # Error 2 == File not found
                    print "Could not find file:", filename
                else:
                    raise
        else:
            # The idea here was to load from the local directory tree
            # first, then from the home directory if directed to do so.
            #
            # This may be changed to something simpler later, but the code
            # is actually quite simple as is; perhaps I'll leave in this
            # "switching" functionality.
            #
            loaded = self.load(os.path.join(
                    "..", jben_globals.CFG_FOLDER, "jben.cfg"))
            if not loaded or self["config_save_target"] == "home":
                env_path = os.getenv(jben_globals.HOME_ENV)
                if env_path:
                    loaded2 = self.load(os.path.join(
                            env_path, jben_globals.CFG_FOLDER, "jben.cfg"))
                    if loaded2:
                        loaded = True

        return loaded

    def save(self, filename=None):
        """Save preferences to a config file.

        If filename is None (default), then J-Ben will save the file based
        on the current install type (standard or mobile).

        Important: If filename is None, and the installation type was
        changed during runtime, then this function will save to both files.
        This is necessary in case two config files are located on a
        system (both standard and mobile), in which case J-Ben will look at
        both files and decide which one to use.

        """
        save_data = __create_config_file_string()
        #print "save_data = [%s]" % save_data

        files = set()
        if filename is None:
            env_path = os.getenv(jben_globals.HOME_ENV)
            if env_path:
                home_path = os.path.join(
                    env_path, jben_globals.CFG_FOLDER, "jben.cfg")
            else:
                home_path = None
            mobile_path = os.path.join(
                "..", jben_globals.CFG_FOLDER, "jben.cfg")

            targets = (self["config_save_target"], original_save_target)
            for target in targets:
                if target == "unset": target = "home"
                if target == "mobile" or not home_path:
                    files.add(mobile_path)
                else:
                    files.add(home_path)
        else:
            files.append(filename)

        for f in files:
            if f:
                try:
                    dirname = os.path.dirname(f)
                    if not os.path.exists(dirname):
                        os.mkdir(dirname)
                    fo = open(f, "w")
                    print "Writing to file:", f
                    fo.write(save_data)
                    fo.close()
                except:
                    # We can add error handlers later...
                    raise

    def set_default_prefs(self):
        """Default preferences are defined here.

        These settings are loaded prior to loading any config file.  Any
        new default settings should be defined here.

        """
        # Changes in Python version
        # 1. JB_DATADIR is now configured in jben_global.py.
        # 2. DSSTR is removed; we will now simply specify "/" as a
        #    directory separator.
        # 3. kanjidicOptions and kanjidicDictionaries have been obsoleted and
        #    replaced with explicit "kdict.render" values.

        self.clear()
        self["config_version"] = Preferences.CURRENT_CONFIG_VERSION
        self["config_save_target"] = "unset"

        # Obsoleted options
        # kanjidicOptions = KDO_READINGS | KDO_MEANINGS
        #                   | KDO_HIGHIMPORTANCE | KDO_VOCABCROSSREF;
        # kanjidicDictionaries = 0;

        # Replaced by the following, more explicit options:

        # KDO_READINGS:
        self["kdict.render.onyomi"] = True
        self["kdict.render.kunyomi"] = True
        self["kdict.render.nanori"] = True
        self["kdict.render.radical_name"] = True

        # KDO_MEANINGS:
        self["kdict.render.meaning"] = True  # ENGLISH
        #options["kdict.render.meaning.fr"] = True  # Example for French

        # KDO_HIGHIMPORTANCE:
        self["kdict.render.stroke_count"] = True
        self["kdict.render.jouyou_grade"] = True
        self["kdict.render.jlpt_level"] = True
        self["kdict.render.frequency"] = True

        # KDO_MULTIRAD:
        self["kdict.render.radical_list"] = False

        # KDO_VOCABCROSSREF:
        self["kdict.render.vocab_cross_ref"] = True

        # KDO_DICTIONARIES:
        self["kdict.render.dictionaries"] = False
        # Additional keys for specific dictionaries are boolean flags tagged onto
        # the end of the above key.
        # Example: kdict.render.dictionaries.kld = True
        # (kld = Kanji Learners' Dictionary)

        # KDO_LOWIMPORTANCE:
        self["kdict.render.jis-208"] = False
        self["kdict.render.jis-212"] = False
        self["kdict.render.jis-213"] = False
        self["kdict.render.unicode"] = False
        self["kdict.render.kangxi_radical"] = False
        self["kdict.render.nelson_radical"] = False
        self["kdict.render.pinyin_roman"] = False
        self["kdict.render.korean"] = False
        self["kdict.render.korean_roman"] = False
        self["kdict.render.cross_ref"] = False

        # KDO_SOD_*:
        self["kdict.render.kanjicafe_sods"] = True
        self["kdict.render.kanjicafe_sodas"] = True

        # Define default paths to supported (and future supported) dicts.
        # J-Ben will automatically append ".gz" and load compressed dictionaries
        # if found.
        # Identifiers are of the form "jben_obj.dict_type.file[#]".  Dicts with the
        # same format should share the same dict_type and add a file number.

        self["kdict.kanjidic2.file"] = (jben_globals.JB_DATADIR
                                        + "/dicts/kanjidic2.xml")
        self["kdict.kanjidic.file"] = (jben_globals.JB_DATADIR
                                       + "/dicts/kanjidic")
        self["kdict.kanjidic.file2"] = (jben_globals.JB_DATADIR
                                        + "/dicts/kanjd212")
        self["kdict.kradfile.file"] = (jben_globals.JB_DATADIR
                                       + "/dicts/kradfile")
        self["kdict.radkfile.file"] = (jben_globals.JB_DATADIR
                                       + "/dicts/radkfile")
        self["wdict.edict.file"] = (jben_globals.JB_DATADIR
                                    + "/dicts/edict")
        self["wdict.edict2.file"] = (jben_globals.JB_DATADIR
                                     + "/dicts/edict2")

        # J-Ben's internal encoding is UTF-8, however most of Jim Breen's non-XML
        # dict files are in EUC-JP.  We should allow the program to support
        # these files.
        self["wdict.edict.file.encoding"] = "euc-jp"
        self["wdict.edict2.file.encoding"] = "euc-jp"
        self["kdict.kanjidic.file.encoding"] = "euc-jp"
        self["kdict.kanjidic.file2.encoding"] = "euc-jp"
        self["kdict.kradfile.file.encoding"] = "euc-jp"
        self["kdict.radkfile.file.encoding"] = "euc-jp"
        # Specify JIS encoding for kanjidic files (jis-208 or jis-212)
        # jis-208 is assumed, so this just means to set it only for kanjd212.
        self["kdict.kanjidic.file2.jispage"] = "jis212"

        self["sod_dir"] = jben_globals.JB_DATADIR + "/sods"

        self["kanjitest.writing.showonyomi"]=True
        self["kanjitest.writing.showkunyomi"]=True
        self["kanjitest.writing.showenglish"]=True
        self["kanjitest.reading.showonyomi"]=False
        self["kanjitest.reading.showkunyomi"]=False
        self["kanjitest.reading.showenglish"]=False
        self["kanjitest.showanswer"]="1"
        self["kanjitest.correctanswer"]="2"
        self["kanjitest.wronganswer"]="3"
        self["kanjitest.stopdrill"]="4"

    def upgrade_config_file(self):
        """Brings settings loaded from previous config file versions up-to-date.

        Generally speaking, this should not need to be edited.  Only when
        an option string has been renamed, or the config file itself changed,
        should this really need to be touched.

        """
        version = self["config_version"]

        # Iterate through the version-wise changes

        if version == "1":
            el.Push(EL_Silent, "Upgrading config file from version 1 to 1.1.")
            # 1 to 1.1:
            # - Add config_save_target setting
            # - Add KANJIDIC2 and KANJD212 default settings
            self["config_save_target"] = "home"
            self["kdict_kanjidic2"] = (jben_globals.JB_DATADIR
                                       + "/dicts/kanjidic2.xml")
            self["kdict_kanjd212"] = (jben_globals.JB_DATADIR
                                      + "/dicts/kanjd212")
            version = "1.1"

        if version == "1.1":
            # 1.1 to 1.2:
            # - Convert xdict_filename to xdict.dicttype_file# format */
            map = {"kdict_kanjidic": "kdict.kanjidic.file",
                   "kdict_kanjd212": "kdict.kanjidic.file2",
                   "kdict_kanjidic2": "kdict.kanjidic2.file",
                   "kdict_kradfile": "kdict.kradfile.file",
                   "kdict_radkfile": "kdict.radkfile.file",
                   "wdict_edict2": "wdict.edict2.file"}
            for old_key, new_key in map.items():
                val = self.get(old_key)
                if val:
                    self[new_key] = val
                    del val[old_key]
            if "kdict.kanjidic.file2" in self.keys():
                self["kdict.kanjidic.file2.jispage"] = "jis212"
            version = "1.2"

        if version == "1.2":
            # This version change doesn't really change anything, but is left in
            # so we don't break anything.
            version = "1.2.1"

        if version == "1.2.1":
            # Updates for J-Ben 2.0
            # 1. Convert kanjidic options/dictionaries int values to normal
            #    options.
            # 2. Rename KanjiList and VocabList to list.kanji and list.vocab
            #    respectively.
            pass
            version = "2.0"

    def __create_config_file_string(self):
        """Creates a complete config file data string for saving to disk."""

        # Format: tab-delimited
        # Example: key	value
        # Notes: First key MUST be "config_version".

        header = "config_version\t%s" % self["config_version"]
        config_strs = []

        # These values are handled specially, so we don't auto-include them.
        excludes = ["config_version", "kanji_list", "vocab_list"]
        other_opts = [(k, v) for k, v in self.items() if k not in excludes]
        for k, v in other_opts:
            if v != '':
                config_strs.append("%s\t%s" % (k, str(v)))
            else:
                print _('Warning: dropping empty setting "%s"!' % k)

        # Append kanji and vocab lists
        # ...

        config_strs.sort()
        config_strs.insert(0, header)
        return "\n".join(config_strs) + "\n"

    def get_dict_path(self):
        # Check folders in sequence for if they're writeable
        # 1. hard-coded, UNIX: /usr/local/share/jben
        # 2. hard-coded, UNIX: /usr/share/jben
        # 3. relative link, global: ../share/jben
        # 4. home folder

        # It does no harm to have dictionaries installed at the global
        # level; it's still up to the users if they want to use them.  So,
        # we'll try to install at the highest priority levels first.

        # Copied from dict_downloader.py:
        # Should default to something like $HOME/.jben.d/dicts for single
        # user install, or ../share/jben/dicts for all user install.
        # ... "All user install" will initially NOT be supported, but will
        # be later.

        if os.name == "nt":
            dirs = []
        else:
            dirs = ["/usr/local/share/jben",
                    "/usr/share/jben"]
        dirs.append("../share/jben")
        env_path = os.getenv(jben_globals.HOME_ENV)
        if env_path:
            dirs.append(os.path.join(env_path, jben_globals.CFG_FOLDER))

        target = None
        for path in dirs:
            if not os.path.exists(path): continue
            path = os.path.join(path, "dicts")
            if (os.path.exists(path) == False) or os.access(path, os.W_OK):
                target = path
                break

        return target
