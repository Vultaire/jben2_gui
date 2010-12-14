# -*- coding: utf-8 -*-

from __future__ import absolute_import


import os
from jben import configure
import jblite.kd2, jblite.jmdict


class DictManager(object):

    """Dictionary manager class."""

    def __init__(self, app):
        self.app = app
        self.kd2 = None
        self.jmdict = None
        self.find_databases()

    @classmethod
    def get_dict_directory(cls):
        """Generator.  Yields candidate dictionary data directories.

        This is needed since dictionaries may be installed either
        system-wide or for a single user.

        """
        for datadir in configure.get_data_dir():
            yield os.path.join(datadir, "dicts")

    @classmethod
    def get_writeable_dict_directory(cls):
        """Returns a writeable dictionary directory.

        Checks permissions and returns either the system or user data
        directory.  Creates the directory if it is not found.

        If a writeable directory cannot be found, an exception is
        raised.

        """
        for datadir in cls.get_dict_directory():
            if os.path.exists(datadir):
                if os.access(datadir, os.W_OK):
                    return datadir
            try:
                os.makedirs(datadir)
                return datadir
            except Exception:
                continue
        raise Exception(
            "Unable to find a writeable dictionary directory.")

    def find_databases(self):
        for datadir in self.get_dict_directory():
            self._find_kanjidic2(datadir)
            self._find_jmdict(datadir)

    def _find_kanjidic2(self, datadir):
        if self.kd2 != None:
            return
        kd2_path = os.path.join(datadir, "kd2.db")
        if os.path.exists(kd2_path):
            # Load an existing database.
            self.kd2 = jblite.kd2.Database(kd2_path)
        else:
            # Try to create the database.
            kd2_xml_path = os.path.join(datadir, "kanjidic2.xml.gz")
            if os.path.exists(kd2_xml_path):
                print "Creating KANJIDIC2 SQLite database; please wait..."
                self.kd2 = jblite.kd2.Database(kd2_path,
                                               init_from_file=kd2_xml_path)
            else:
                self.kd2 = None

    def _find_jmdict(self, datadir):
        if self.jmdict != None:
            return
        jmdict_path = os.path.join(datadir, "jmdict.db")
        if os.path.exists(jmdict_path):
            self.jmdict = jblite.jmdict.Database(jmdict_path)
        else:
            jmdict_xml_path = os.path.join(datadir, "JMdict.gz")
            if os.path.exists(jmdict_xml_path):
                print "Creating JMdict SQLite database; please wait..."
                self.jmdict = jblite.jmdict.Database(
                    jmdict_path, init_from_file=jmdict_xml_path)
            else:
                self.jmdict = None

    def all_dicts_found(self):
        return (self.kd2 is not None) and (self.jmdict is not None)

    def jmdict_found(self):
        return (self.jmdict is not None)

    def kd2_found(self):
        return (self.kd2 is not None)

    def get_needed_dict_names(self):
        """Returns a list of file names of any missing dictionary files."""
        needed = []
        if not self.kd2_found():
            needed.append("kanjidic2.xml.gz")
        if not self.jmdict_found():
            needed.append("JMdict.gz")
        return needed
