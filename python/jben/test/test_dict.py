import unittest
from jben.dict import DictManager
from jben import configure
import os


class ClassFunctions(unittest.TestCase):

    @unittest.skipUnless(os.name == "posix", "This test is for POSIX only.")
    def test_get_dict_dir_posix(self):
        # Get a list of candidate directories
        dict_dirs = list(DictManager.get_dict_directory())

        # We should get 2 entries: a system and user directory.
        self.assertEqual(len(dict_dirs), 2)

        pkgdatadir = configure.pkgdatadir
        self.assertTrue(dict_dirs[0].startswith(pkgdatadir))

        user_data_dir = configure.get_user_data_dir()
        self.assertTrue(dict_dirs[1].startswith(user_data_dir))

    @unittest.skipUnless(os.name == "nt", "This test is for Windows only.")
    def test_get_dict_dir_nt(self):
        # Get a list of candidate directories
        dict_dirs = list(DictManager.get_dict_directory())

        # We should get 2 entries: a system and user directory.
        self.assertEqual(len(dict_dirs), 2)

        pkgdatadir = configure.pkgdatadir
        self.assertTrue(dict_dirs[0].startswith("data"))

        user_data_dir = configure.get_user_data_dir()
        self.assertTrue(dict_dirs[1].startswith(user_data_dir))

#    def test_get_writeable_dir(self):
#        # This test *assumes* that we're not running as root.
#        DictManager
