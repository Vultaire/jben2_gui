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

    def find_databases(self):
        datadir = configure.get_datadir()

        kd2_path = os.path.join(datadir, "kd2.db")
        if os.path.exists(kd2_path):
            # Load an existing database.
            self.kd2 = jblite.kd2.Database(kd2_path)
        else:
            # Try to create the database.
            kd2_xml_path = os.path.join(datadir, "kanjidic2.xml.gz")
            if os.path.exists(kd2_xml_path):
                self.kd2 = jblite.kd2.Database(kd2_path,
                                               init_from_file=kd2_xml_path)
            else:
                self.kd2 = None

        jm_path = os.path.join(datadir, "jmdict.db")
        if os.path.exists(jm_path):
            self.jmdict = jblite.jmdict.Database(jm_path)
        else:
            jmdict_xml_path = os.path.join(datadir, "jmdict.gz")
            if os.path.exists(jmdict_xml_path):
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
