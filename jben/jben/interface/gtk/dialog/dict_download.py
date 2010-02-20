# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: jben/gui/dialog/kanjilisteditor.py
# Author: Paul Goins
# Created on: 26 Nov 2008

from __future__ import absolute_import

import gtk
from ..widget.storedsize import StoredSizeDialog
from jben.dict_downloader import static_mirror_list


class DictDownload(StoredSizeDialog):

    def __init__(self, parent):
        StoredSizeDialog.__init__(
            self, "gui.dialog.dict_download.size", -1, -1,
            title=_("Download dictionaries"),
            parent=parent
            )

        self._layout()

    def _layout(self):
        pass
