# -*- coding: utf-8 -*-

from __future__ import absolute_import

import gtk


class InfoMessage(gtk.MessageDialog):

    def __init__(self, parent=None, title="", message="",
                 type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_YES_NO,
                 default_button=None):
        gtk.MessageDialog.__init__(self, parent,
                                   gtk.DIALOG_MODAL, type,
                                   buttons, message)
	self.set_title(title)
        if default_button:
            if default_button.lower() == "yes":
                self.set_default_response(gtk.RESPONSE_YES)
            elif default_button.lower() == "yes":
                self.set_default_response(gtk.RESPONSE_NO)

def show_message_yn(parent, title, message, default_button=None):
    """Convenience function intended for displaying modal dialogs."""
    im = InfoMessage(parent, title, message, default_button=default_button)
    result = im.run()
    im.destroy()
    return True if result == gtk.RESPONSE_YES else False
