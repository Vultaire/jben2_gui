#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: jben/gui/dialog/kanjilisteditor.py
# Author: Paul Goins
# Created on: 26 Nov 2008

from __future__ import absolute_import

import gtk
from ..widget.storedsize import StoredSizeDialog

from .addkanjibyjouyou import AddKanjiByJouyouDialog
from .addkanjibyjlpt import AddKanjiByJlptDialog
from .addkanjibyfreq import AddKanjiByFreqDialog


class EditBox(gtk.TextView):

    def __init__(self):
        gtk.TextView.__init__(self)
        self.set_accepts_tab(False)
        self.set_wrap_mode(gtk.WRAP_WORD_CHAR)

        self.modified = False

        self.get_buffer().connect("changed", self.on_text_changed)

    def on_text_changed(self, widget):
        print "EditBox.on_text_changed"
        self.modified = True


class BaseButton(gtk.Button):

    def __init__(self, label, edit_box):
        gtk.Button.__init__(self, label)
        self.connect("clicked", self.on_clicked, edit_box)

    def _get_parent_window(self):
        parent = self.get_parent()
        while True:
            if isinstance(parent, gtk.Window):
                return parent
            elif parent == None:
                raise Exception(
                    "Expected parent object, but found None instead.")
            parent = parent.get_parent()

    def on_clicked(self, widget, edit_box):
        print "BaseButton clicked"


class AddFromFile(BaseButton):

    def __init__(self, edit_box):
        BaseButton.__init__(self, _("From _File"), edit_box)

    def on_clicked(self, widget, edit_box):
        parent=self._get_parent_window()
        dialog = gtk.FileChooserDialog(
            parent=parent,
            buttons=(
                gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                gtk.STOCK_OK, gtk.RESPONSE_OK))
        result = dialog.run()
        if result == gtk.RESPONSE_OK:
            filename = dialog.get_filename()
            if isinstance(filename, str):
                print "FILE SELECTED:", repr(filename)
                # Open file
                # Make a set of all unique characters
                # Limit characters to Japanese characters
                # Update edit box
        dialog.destroy()


class AddByJouyou(BaseButton):

    def __init__(self, edit_box):
        BaseButton.__init__(self, _("By Jouyou _Grade"), edit_box)

    def on_clicked(self, widget, edit_box):
        parent = self._get_parent_window()
        dialog = AddKanjiByJouyouDialog(parent)
        result = dialog.run()
        if result == gtk.RESPONSE_OK:
            low, high = dialog.get_grades()
            print "TODO: Add kanji from Jouyou grades %d to %d" % (low, high)
            # Get kanji in specified range
            # Merge lists
            # Update edit box
        dialog.destroy()

class AddByJlpt(BaseButton):

    def __init__(self, edit_box):
        BaseButton.__init__(self, _("By _JLPT Level"), edit_box)

    def on_clicked(self, widget, edit_box):
        parent = self._get_parent_window()
        dialog = AddKanjiByJlptDialog(parent)
        result = dialog.run()
        if result == gtk.RESPONSE_OK:
            low, high = dialog.get_grades()
            print "TODO: Add kanji from JLPT grades %d to %d" % (low, high)
            # Get kanji in specified range
            # Merge lists
            # Update edit box
        dialog.destroy()


class AddByFreq(BaseButton):

    def __init__(self, edit_box):
        BaseButton.__init__(self, _("By Fre_quency"), edit_box)

    def on_clicked(self, widget, edit_box):
        parent = self._get_parent_window()
        dialog = AddKanjiByFreqDialog(parent)
        result = dialog.run()
        if result == gtk.RESPONSE_OK:
            low, high = dialog.get_freq_range()
            print "TODO: Add kanji between frequency rankings %d and %d." \
                % (low, high)
            # Get kanji in specified range
            # Merge lists
            # Update edit box
        dialog.destroy()


class SortByJouyou(BaseButton):

    def __init__(self, edit_box):
        BaseButton.__init__(self, _("By Jouyou G_rade"), edit_box)

    def on_clicked(self, widget, edit_box):
        print "sort.by_jouyou clicked"


class SortByJlpt(BaseButton):

    def __init__(self, edit_box):
        BaseButton.__init__(self, _("By J_LPT Level"), edit_box)

    def on_clicked(self, widget, edit_box):
        print "sort.by_jlpt clicked"


class SortByFreq(BaseButton):

    def __init__(self, edit_box):
        BaseButton.__init__(self, _("By Freq_uency"), edit_box)

    def on_clicked(self, widget, edit_box):
        print "sort.by_freq clicked"


class DirectEdit(gtk.CheckButton):

    def __init__(self, edit_box):
        gtk.CheckButton.__init__(self, _("_Edit directly"))
        self.connect("toggled", self.on_toggled, edit_box)

        # Call once to set initial status appropriately.
        self.on_toggled(self, edit_box)

    def on_toggled(self, widget, edit_box):
        state = widget.get_active()
        edit_box.set_sensitive(state)


class EditWindow(gtk.ScrolledWindow):

    def __init__(self, edit_box):
        gtk.ScrolledWindow.__init__(self)
        self.set_shadow_type(gtk.SHADOW_IN)
        self.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.add(edit_box)


class ShadowedFrame(gtk.Frame):

    def __init__(self, *args, **kwargs):
        gtk.Frame.__init__(self, *args, **kwargs)
        self.set_shadow_type(gtk.SHADOW_IN)


class AddFrame(ShadowedFrame):

    def __init__(self, edit_box):
        ShadowedFrame.__init__(self, _("Add Kanji"))
        box = gtk.VBox()
        for button_class in (AddFromFile, AddByJouyou, AddByJlpt, AddByFreq):
            button = button_class(edit_box)
            box.pack_start(button, expand=False)
        self.add(box)


class SortFrame(ShadowedFrame):

    def __init__(self, edit_box):
        ShadowedFrame.__init__(self, _("Sort Kanji"))
        box = gtk.VBox()
        for button_class in (SortByJouyou, SortByJlpt, SortByFreq):
            button = button_class(edit_box)
            box.pack_start(button, expand=False)
        self.add(box)


class SideButtons(gtk.VBox):

    def __init__(self, edit_box):
        gtk.VBox.__init__(self, spacing=5)

        add_frame = AddFrame(edit_box)
        sort_frame = SortFrame(edit_box)

        for frame in (add_frame, sort_frame):
            self.pack_start(frame, expand=False)

        direct_edit = DirectEdit(edit_box)
        align = gtk.Alignment(xalign=1.0)
        align.add(direct_edit)
        self.pack_start(align)


class DialogKanjiListEditor(StoredSizeDialog):
    def __init__(self, parent):
        StoredSizeDialog.__init__(self, "gui.kanjilisteditor.size", -1, -1,
                                  _("Kanji List Editor"), parent)

        edit_box = EditBox()

        edit_window = EditWindow(edit_box)
        side_buttons = SideButtons(edit_box)

        main_box = gtk.HBox(spacing=5)
        main_box.pack_start(side_buttons, expand=False)
        main_box.pack_start(edit_window)

        self.vbox.set_spacing(5)
        self.vbox.pack_start(main_box)
        self.vbox.show_all()

        ok_button = gtk.Button(stock=gtk.STOCK_OK)
        cancel_button = gtk.Button(stock=gtk.STOCK_CANCEL)
        apply_button = gtk.Button(stock=gtk.STOCK_APPLY)

        ok_button.connect("clicked", self.on_ok_clicked)
        cancel_button.connect("clicked", self.on_cancel_clicked)
        apply_button.connect("clicked", self.on_apply_clicked)

        for button in cancel_button, apply_button, ok_button:
            self.action_area.pack_start(button)
        self.action_area.show_all()

        self.set_has_separator(False)

    def apply(self):
        print "apply()ing changes"

    def on_cancel_clicked(self, widget):
        self.response(gtk.RESPONSE_CANCEL)

    def on_apply_clicked(self, widget):
        self.apply()

    def on_ok_clicked(self, widget):
        self.apply()
        self.response(gtk.RESPONSE_OK)
