#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: preferences.py
# Author: Paul Goins
# Created on: 20 December 2008

# NOTE: This module contains code written by other people but
# available (to the best of my knowledge) under a compatible license.
# Such code is clearly marked.

from __future__ import absolute_import, with_statement

import sys, os, re, traceback, warnings
from jben import jben_globals
from jben.alphanum import make_alphanum_list


class Preferences(dict):

    CURRENT_CONFIG_VERSION = "2.0"

    def __init__(self, app):
        dict.__init__(self)
        self.app = app
        self.fname = self.get_filename()
        loaded = self.load()
        if loaded and self.is_outdated():
            pass  # no logic implemented yet
        self['config_version'] = self.CURRENT_CONFIG_VERSION

    def get_filename(self):
        confdir = self.app.get_settings_dir()
        fname = os.path.join(confdir, "jben.cfg")
        if not os.path.exists(confdir):
            os.mkdir(confdir)
        if os.path.exists(fname):
            if not os.access(fname, os.R_OK):
                raise Exception("No read access to config file.")
            elif not os.access(fname, os.W_OK):
                warnings.warn("Cannot write to config file.")
        else:
            if not os.access(confdir, os.W_OK):
                raise Exception(
                    "No config file, and no write permissions to create one")
        return fname

    def is_outdated(self):
        version = make_alphanum_list(self.get('config_version', "0"))
        return version < make_alphanum_list(self.CURRENT_CONFIG_VERSION)

    def load(self):
        try:
            with open(self.fname) as ifile:
                lines = ifile.readlines()
            for line in lines:
                line = line.strip()
                if not line or line[0] in ("#", ";"):
                    continue
                k, v = re.split("[ \t=:]+", line, 1)
                if k and v:
                    v2 = v.lower().strip()
                    if v2 in ("true", "false"):
                        self[k] = (v2 == "true")
                    else:
                        self[k] = v
        except IOError:
            return False
        return True

    def save(self):
        # TO DO: handle exceptions gracefully
        save_data = self.dump()
        with open(self.fname, "w") as ofile:
            ofile.write(save_data)

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
