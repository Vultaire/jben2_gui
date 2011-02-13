# -*- coding: utf-8 -*-
"""Dialog for adding kanji by Jouyou grade level."""

from __future__ import absolute_import

import gtk
from ..widget.storedsize import StoredSizeDialog
from ..widget.comboboxtext import ComboBoxText
from ..widget.infomessage import show_message


GENERAL_USAGE = 8
JINMEIYOU = 9
# Other codes could come here...
UNCATEGORIZED = 0xFF


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

        Return value is the integer code selected.

        """
        index = self.get_active()
        if index < 6:
            return index + 1
        elif index == 6:
            return GENERAL_USAGE
        elif index == 7:
            return JINMEIYOU
        else:
            return UNCATEGORIZED


class AddKanjiByJouyouDialog(gtk.Dialog):

    def __init__(self, parent):
        gtk.Dialog.__init__(self, _("Add Kanji By Jouyou Grade"), parent),

        self.low_grade = JouyouComboBox()
        self.high_grade = JouyouComboBox()

        low_label = gtk.Label(_("Low grade:"))
        high_label = gtk.Label(_("High grade:"))

        tbl = gtk.Table(2, 2)

        for i, label in enumerate((low_label, high_label)):
            align = gtk.Alignment(xalign=1.0, yalign=0.5)
            align.add(label)
            tbl.attach(align, 0, 1, i, i+1, xpadding=5, ypadding=5)
        for i, combo in enumerate((self.low_grade, self.high_grade)):
            tbl.attach(combo, 1, 2, i, i+1, xpadding=5, ypadding=5)

        self.vbox.set_spacing(5)
        self.vbox.pack_start(tbl)
        self.vbox.show_all()

        buttons=[
            (gtk.STOCK_CANCEL, self.on_cancel_clicked),
            (gtk.STOCK_OK, self.on_ok_clicked),
            ]

        for stock_code, handler in buttons:
            button = gtk.Button(stock=stock_code)
            button.connect("clicked", handler)
            self.action_area.pack_start(button)

        self.action_area.show_all()

    def on_cancel_clicked(self, widget):
        self.response(gtk.RESPONSE_CANCEL)

    def on_ok_clicked(self, widget):
        grade_min, grade_max = self.get_grades()

        if grade_min <= grade_max:
            self.response(gtk.RESPONSE_OK)
        else:
            show_message(
                self, _(u"Invalid range selected"),
                _(u"The upper grade cannot be lower than the lower grade."))

    def get_grades(self):
        grade_min = self.low_grade.get_grade()
        grade_max = self.high_grade.get_grade()
        return (grade_min, grade_max)
