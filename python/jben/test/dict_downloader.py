# -*- coding: utf-8 -*-

import unittest, time
import jben.dict_downloader as dd


class Test(unittest.TestCase):

    def test_get_mirror_list_offline(self):
        ml = dd.get_mirror_list(from_inet=False)
        self.assertTrue(len(ml) > 0)

    def test_get_mirror_list_online(self):
        ml = dd.get_mirror_list(from_inet=True)
        self.assertTrue(len(ml) > 0)

class TestINet(unittest.TestCase):

    """Tests to be run sparingly since they rely on Internet servers."""

    def test_download_dict(self):
        fname = "kanjidic.gz"
        dd.download_dict(fname)
        # Maybe add checking for file existance afterwards?
        # For now, if the function runs without raising an exception,
        # it's good enough.


if __name__ == "__main__":
    unittest.main()
