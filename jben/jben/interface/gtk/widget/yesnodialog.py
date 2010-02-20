# -*- coding: utf-8 -*-

from __future__ import absolute_import

import gtk


class InfoMessage(gtk.MessageDialog):

    def __init__(self, parent=None, title="", message="",
                 type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_YES_NO):
        gtk.MessageDialog.__init__(self, parent,
                                   gtk.DIALOG_MODAL, type,
                                   buttons, message)
	self.set_title(title)


def show_message_yn(parent, title, message):
    """Convenience function intended for displaying modal dialogs."""
    im = InfoMessage(parent, title, message)
    result = im.run()
    im.destroy()
    return True if result == gtk.RESPONSE_YES else False
