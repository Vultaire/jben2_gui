# -*- coding: utf-8 -*-

from __future__ import absolute_import

import gtk


class InfoMessage(gtk.MessageDialog):

    def __init__(self, parent=None, title="", message="",
                 type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK):
        gtk.MessageDialog.__init__(self, parent,
                                   gtk.DIALOG_MODAL, type,
                                   buttons, message)
	self.set_title(title)


def show_message(parent, title, message):
    """Convenience function intended for displaying modal dialogs."""
    im = InfoMessage(parent, title, message)
    im.run()
    im.destroy()
