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
from jben.alphanum import make_alphanum_list


class Preferences(dict):

    CURRENT_CONFIG_VERSION = "2.0"

    def __init__(self):
        dict.__init__(self)
        self.load()
        # This variable will be set to the contents of
        # prefs["config_save_target"] when a config file is loaded,
        # in order to track runtime changes.
        self.original_save_target = self["config_save_target"]

    def is_outdated(self):
        version = make_alphanum_list(self.get('config_version', "0"))
        return version < make_alphanum_list(Preferences.CURRENT_CONFIG_VERSION)

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

    def load(self, filename=None):
        """Load preferences from a config file.

        If filename is None (default), then J-Ben will search for a config
        file in the program's parent directory (important for self-contained
        "mobile" installs), followed by the user's home directory.

        """
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
        save_data = self.dump()
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

            targets = (self["config_save_target"], self.original_save_target)
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

    def dump(self):
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


class DictEntry(object):

    """Class for dictionary preference entries."""

    def __init__(self, filename, format=None, encoding=None):
        self.filename = filename
        self.format = format if format else self._get_format()
        self.encoding = encoding if encoding else self._get_encoding()

    def _get_format(self):
        """Automatic format selection function."""
        # Automatic format selection based on file name
        filename = os.path.basename(self.filename).split(".")[0].lower()
        if filename.startswith("edict2"):
            # EDICT2 parser is not yet complete in jbparse library.
            raise NotImplementedError
        if filename.startswith("edict"): return "edict"
        if filename.startswith("jmdict"): return "jmdict"
        if filename.startswith("kanjidic2"): return "kanjidic2"
        if any(filename.startswith(s) for s in ["kanjidic", "kanjd212"]):
            return "kanjidic"
        raise Exception('Could not determine dictionary format based on '
                        'filename "%s"' % filename)

    def _get_encoding(self):
        """Automatic encoding selection function."""
        # Automatic encoding selection based on file name
        filename = self.filename.split(".")[0].lower()
        if any([filename.startswith(s) for s in ["jmdict", "kanjidic2"]]):
            return "utf-8"
        if any([filename.startswith(s)
                  for s in ["edict", "kanjidic", "kanjd212"]]):
            return "euc-jp"
        # Default encoding...  I need to check what other
        # EDICT-style dictionaries are using nowadays.  My
        # strong preference is to do everything as UTF-8.
        return "utf-8"
