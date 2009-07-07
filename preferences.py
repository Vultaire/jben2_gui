#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: preferences.py
# Author: Paul Goins
# Created on: 20 December 2008

from jben_global import *
import re

options = {}
"""Maps preference key strings to stored option values."""

original_save_target = None
"""This variable will be set to the contents of options["config_save_target"]
when a config file is loaded, in order to track runtime changes.
"""

__CURRENT_CONFIG_VERSION = "2.0"
"""The current version of the config file."""

def load(filename=None):
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
                            options[k] = (v2 == "true")
                        else:
                            options[k] = v
                except ValueError:
                    print _("Warning: unable to split line: %s" % line)
            original_save_target = options["config_save_target"]
        except IOError, e:
            if e.args[0] == 2:  # Error 2 == File not found
                print "Could not find file:", filename
            else:
                raise
    else:
        loaded = load("../%s/jben.cfg" % CFG_FOLDER)
        if not loaded or options["config_save_target"] == "home":
            env_path = os.getenv(HOME_ENV)
            if env_path:
                loaded2 = load("%s/%s/jben.cfg" % (env_path, CFG_FOLDER))
                if loaded2:
                    loaded = True

    return loaded

def save(filename=None):
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
        env_path = os.getenv(HOME_ENV)
        if env_path: home_path = "%s/%s/jben.cfg" % (env_path, CFG_FOLDER)
        else: home_path = None
        mobile_path = "../%s/jben.cfg" % CFG_FOLDER

        targets = (options["config_save_target"], original_save_target)
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

def set_default_prefs():
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

    options.clear()
    options["config_version"] = __CURRENT_CONFIG_VERSION
    options["config_save_target"] = "unset"

    # Obsoleted options
    # kanjidicOptions = KDO_READINGS | KDO_MEANINGS
    #                   | KDO_HIGHIMPORTANCE | KDO_VOCABCROSSREF;
    # kanjidicDictionaries = 0;

    # Replaced by the following, more explicit options:

    # KDO_READINGS:
    options["kdict.render.onyomi"] = True
    options["kdict.render.kunyomi"] = True
    options["kdict.render.nanori"] = True
    options["kdict.render.radical_name"] = True

    # KDO_MEANINGS:
    options["kdict.render.meaning"] = True  # ENGLISH
    #options["kdict.render.meaning.fr"] = True  # Example for French

    # KDO_HIGHIMPORTANCE:
    options["kdict.render.stroke_count"] = True
    options["kdict.render.jouyou_grade"] = True
    options["kdict.render.jlpt_level"] = True
    options["kdict.render.frequency"] = True

    # KDO_MULTIRAD:
    options["kdict.render.radical_list"] = False

    # KDO_VOCABCROSSREF:
    options["kdict.render.vocab_cross_ref"] = True

    # KDO_DICTIONARIES:
    options["kdict.render.dictionaries"] = False
    # Additional keys for specific dictionaries are boolean flags tagged onto
    # the end of the above key.
    # Example: kdict.render.dictionaries.kld = True
    # (kld = Kanji Learners' Dictionary)

    # KDO_LOWIMPORTANCE:
    options["kdict.render.jis-208"] = False
    options["kdict.render.jis-212"] = False
    options["kdict.render.jis-213"] = False
    options["kdict.render.unicode"] = False
    options["kdict.render.kangxi_radical"] = False
    options["kdict.render.nelson_radical"] = False
    options["kdict.render.pinyin_roman"] = False
    options["kdict.render.korean"] = False
    options["kdict.render.korean_roman"] = False
    options["kdict.render.cross_ref"] = False

    # KDO_SOD_*:
    options["kdict.render.kanjicafe_sods"] = True
    options["kdict.render.kanjicafe_sodas"] = True

    # Define default paths to supported (and future supported) dicts.
    # J-Ben will automatically append ".gz" and load compressed dictionaries
    # if found.
    # Identifiers are of the form "jben_obj.dict_type.file[#]".  Dicts with the
    # same format should share the same dict_type and add a file number.

    options["kdict.kanjidic2.file"] = JB_DATADIR + "/dicts/kanjidic2.xml"
    options["kdict.kanjidic.file"] = JB_DATADIR + "/dicts/kanjidic"
    options["kdict.kanjidic.file2"] = JB_DATADIR + "/dicts/kanjd212"
    options["kdict.kradfile.file"] = JB_DATADIR + "/dicts/kradfile"
    options["kdict.radkfile.file"] = JB_DATADIR + "/dicts/radkfile"
    options["wdict.edict.file"] = JB_DATADIR + "/dicts/edict"
    options["wdict.edict2.file"] = JB_DATADIR + "/dicts/edict2"

    # J-Ben's internal encoding is UTF-8, however most of Jim Breen's non-XML
    # dict files are in EUC-JP.  We should allow the program to support
    # these files.
    options["wdict.edict.file.encoding"] = "euc-jp"
    options["wdict.edict2.file.encoding"] = "euc-jp"
    options["kdict.kanjidic.file.encoding"] = "euc-jp"
    options["kdict.kanjidic.file2.encoding"] = "euc-jp"
    options["kdict.kradfile.file.encoding"] = "euc-jp"
    options["kdict.radkfile.file.encoding"] = "euc-jp"
    # Specify JIS encoding for kanjidic files (jis-208 or jis-212)
    # jis-208 is assumed, so this just means to set it only for kanjd212.
    options["kdict.kanjidic.file2.jispage"] = "jis212"

    options["sod_dir"] = JB_DATADIR + "/sods"

    options["kanjitest.writing.showonyomi"]=True
    options["kanjitest.writing.showkunyomi"]=True
    options["kanjitest.writing.showenglish"]=True
    options["kanjitest.reading.showonyomi"]=False
    options["kanjitest.reading.showkunyomi"]=False
    options["kanjitest.reading.showenglish"]=False
    options["kanjitest.showanswer"]="1"
    options["kanjitest.correctanswer"]="2"
    options["kanjitest.wronganswer"]="3"
    options["kanjitest.stopdrill"]="4"

def upgrade_config_file():
    """Brings settings loaded from previous config file versions up-to-date.

    Generally speaking, this should not need to be edited.  Only when
    an option string has been renamed, or the config file itself changed,
    should this really need to be touched.

    """
    version = options["config_version"]

    # Iterate through the version-wise changes

    if version == "1":
        el.Push(EL_Silent, "Upgrading config file from version 1 to 1.1.")
        # 1 to 1.1:
        # - Add config_save_target setting
        # - Add KANJIDIC2 and KANJD212 default settings
        options["config_save_target"] = "home"
        options["kdict_kanjidic2"] = JB_DATADIR + "/dicts/kanjidic2.xml"
        options["kdict_kanjd212"] = JB_DATADIR + "/dicts/kanjd212"
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
            val = options.get(old_key)
            if val:
                options[new_key] = val
                del val[old_key]
        if "kdict.kanjidic.file2" in options.keys():
            options["kdict.kanjidic.file2.jispage"] = "jis212"
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

    version = __CURRENT_CONFIG_VERSION

def __create_config_file_string():
    """Creates a complete config file data string for saving to disk."""

    # Format: tab-delimited
    # Example: key	value
    # Notes: First key MUST be "config_version".

    header = "config_version\t%s" % options["config_version"]
    config_strs = []

    # These values are handled specially, so we don't auto-include them.
    excludes = ["config_version", "kanji_list", "vocab_list"]
    other_opts = [(k, v) for k, v in options.items() if k not in excludes]
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
