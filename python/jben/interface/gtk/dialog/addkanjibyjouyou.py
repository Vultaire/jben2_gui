# -*- coding: utf-8 -*-
"""Dialog for adding kanji by Jouyou grade level."""

from __future__ import absolute_import

import gtk, gobject
from ..widget.storedsize import StoredSizeDialog


# J-Ben 1 used GtkComboBoxText.  PyGTK does not have this specific
# subclass for some reason, although the same class exists both in
# GTKmm and in the original GTK+.
#
# There appears to be somewhat of an equivalent via
# gtk.combo_box_new_text, but this does not allow subclassing.
#
# There is, however, a gtk.ComboBoxEntry in PyGTK.  This seems to
# parallel gtk_combo_box_text_new_with_entry in the C API.
# However, I don't want the Entry...
#
# Fine: let's do things by hand.  It can't be too hard.
#
# AFTER DOING IT:
#
# This was not simple.  The documentation is abysmal; the official GTK
# docs are very terse with few examples (the only ComboBox example I
# could find was for a deprecated API!), and the PyGTK example works
# but doesn't provide any explanation of what's going on.
#
# I guess it shows: people willing to write docs are always welcome on
# OSS projects :)
#
# Anyway, I got this working, so I'll use my version.


# Alternative: There is a helper function which auto-creates a
# ComboBox of the form we want, but we can't subclass this.  We'd have
# to encapsulate the object which makes it slightly less convenient
# for packing into the rest of the interface.


class ComboBoxText(gtk.ComboBox):

    def __init__(self, strs=[]):
        # The next 5 lines are pretty much copied from the PyGTK
        # example:
        # http://www.pygtk.org/docs/pygtk/class-gtkcombobox.html I've
        # added comments to make up for the lack of explanation in the
        # official docs.

        # Create model and attach it to a new ComboBox.
        self.__model = gtk.ListStore(gobject.TYPE_STRING)
        gtk.ComboBox.__init__(self, self.__model)

        # Create renderer
        renderer = gtk.CellRendererText()

        # Map renderer to CellLayout
        self.pack_start(renderer, True)
        self.add_attribute(renderer, 'text', 0)

        # From here is my code:
        for s in strs:
            self.append_text(s)

        if len(strs) > 0:
            self.set_active(0)

    def append_text(self, value):
        itr = self.__model.append()
        self.__model.set_value(itr, 0, value)

    # Other interfaces could be added, but I don't need them.


GENERAL_USAGE = 8
JINMEIYOU = 9


class JouyouComboBox(ComboBoxText):

    strs = [
	_("Jouyou Kanji Grade 1"),
	_("Jouyou Kanji Grade 2"),
	_("Jouyou Kanji Grade 3"),
	_("Jouyou Kanji Grade 4"),
	_("Jouyou Kanji Grade 5"),
	_("Jouyou Kanji Grade 6"),
	_("Jouyou Kanji, General Usage"),
	_("Jinmeiyou Kanji (for names)"),
	_("Non-Jouyou/Non-Jinmeiyou Kanji")
        ]

    def __init__(self):
        ComboBoxText.__init__(self, self.strs)

    def get_grade(self):
        """Returns grade as defined in KANJIDIC/KANJIDIC2.

        Grades are 1-6, representing elementary school grades,
        followed by several special codes.

        Return value is the integer code, or None if the kanji has no
        category.

        """
        index = self.get_active()
        if index < 6:
            return index + 1
        elif index == 6:
            return GENERAL_USAGE
        elif index == 7:
            return JINMEIYOU
        return None


class LowGradeComboBox(JouyouComboBox):
    pass


class HighGradeComboBox(JouyouComboBox):
    pass


class AddKanjiByJouyouDialog(StoredSizeDialog):

    def __init__(self, parent):
        StoredSizeDialog.__init__(
            self, "gui.addkanjibyjouyou.size", -1, -1,
            _("Add Kanji By Jouyou Grade"),
            parent,
            #flags=gtk.DIALOG_NO_SEPARATOR,  # No difference (on Windows)?
            buttons=(
                gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                gtk.STOCK_OK, gtk.RESPONSE_OK),
            )

        self.low_grade = LowGradeComboBox()
        self.high_grade = HighGradeComboBox()

        self.vbox.set_spacing(5)
        for control in (self.low_grade, self.high_grade):
            self.vbox.pack_start(control)
        self.vbox.show_all()
