#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: window_kanjihwsearch.py
# Author: Paul Goins
# Created on: 25 Nov 2008

from __future__ import absolute_import

import gtk

from jben.jben_global import *
from .widget_hwpad import WidgetHWPad
from .tab_worddict import TabWordDict
from .tab_kanjidict import TabKanjiDict
from .window_kanjihwsearch import WindowKanjiHWSearch
from .dialog_vocablisteditor import DialogVocabListEditor
from .dialog_kanjilisteditor import DialogKanjiListEditor
from .dialog_preferences import DialogPreferences
from .widget_storedsize import StoredSizeWindow

class InfoMessage(gtk.MessageDialog):
    def __init__(self, parent=None, title="", message="",
                 type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK):
        gtk.MessageDialog.__init__(self, parent,
                                   gtk.DIALOG_MODAL, type,
                                   buttons, message)
	self.set_title(title)

class WindowMain(StoredSizeWindow):
    """The main GUI of J-Ben."""

    def __init__(self, param="gui.main.size"):
        StoredSizeWindow.__init__(self, param, 600, 400, gtk.WINDOW_TOPLEVEL)
        self.connect("destroy", self.destroy)
        self.set_title(PROGRAM_NAME)

        self.menu = self.create_menu()
        self.children = self.create_children()

        layout = gtk.VBox(spacing = 5)
        layout.pack_start(self.menu, expand = False)
        layout.pack_start(self.children)

        self.add(layout)

    def destroy(self, widget, data = None):
        gtk.main_quit()

    def create_menu(self):
        ag = gtk.ActionGroup("jben.ag")
        ag.add_actions(
            [("MenuFile", None, _("_File"), None, None, None),

             ("MenuFileQuit", gtk.STOCK_QUIT, None,
              None, None, self.on_menu_file_quit),

             ("MenuEdit", None, _("_Edit"),
              None, None, None),

             ("MenuEditVocab", None, _("_Vocab Study List"),
              None, None, self.on_menu_edit_vocab),

             ("MenuEditKanji", None, _("_Kanji Study List"),
              None, None, self.on_menu_edit_kanji),

             ("MenuEditPrefs", gtk.STOCK_PREFERENCES, None,
              None, None, self.on_menu_edit_prefs),

             ("MenuPractice", None, _("_Practice"), None, None, None),

             ("MenuPracticeKanji", None, _("_Kanji"),
              None, None, self.on_menu_practice_kanji),

             ("MenuTools", None, _("_Tools"), None, None, None),

             ("MenuToolsHand", None, _("_Handwriting Recognition for Kanji"),
              None, None, self.on_menu_tools_hand),

             ("MenuToolsKanjiSearch", None, _("_Kanji Search"),
              None, None, self.on_menu_tools_kanji_search),

             ("MenuHelp", None, _("_Help"), None, None, None),

             ("MenuHelpAbout", gtk.STOCK_ABOUT,
              None, None, None, self.on_menu_help_about),

             ("MenuHelpLicense", None, _("_License Information..."),
              None, None, self.on_menu_help_license)])

        uim = gtk.UIManager()
        uim.insert_action_group(ag, -1)
        uim.add_ui_from_string(
            "<ui>"
            "  <menubar name='MenuBar'>"
            "    <menu action='MenuFile'>"
            "      <menuitem action='MenuFileQuit'/>"
            "    </menu>"
            "    <menu action='MenuEdit'>"
            "      <menuitem action='MenuEditVocab'/>"
            "      <menuitem action='MenuEditKanji'/>"
            "      <separator/>"
            "      <menuitem action='MenuEditPrefs'/>"
            "    </menu>"
            "    <menu action='MenuPractice'>"
            "      <menuitem action='MenuPracticeKanji'/>"
            "    </menu>"
            "    <menu action='MenuTools'>"
            "      <menuitem action='MenuToolsHand'/>"
            "      <menuitem action='MenuToolsKanjiSearch'/>"
            "    </menu>"
            "    <menu action='MenuHelp'>"
            "      <menuitem action='MenuHelpAbout'/>"
            "      <menuitem action='MenuHelpLicense'/>"
            "    </menu>"
            "  </menubar>"
            "</ui>")
        self.add_accel_group(uim.get_accel_group())
        return uim.get_widget("/MenuBar")

    def create_children(self):
        tabs = gtk.Notebook()
        worddict = TabWordDict()
        kanjidict = TabKanjiDict()
        tabs.append_page(worddict, gtk.Label(_("Word Dictionary")))
        tabs.append_page(kanjidict, gtk.Label(_("Kanji Dictionary")))
        return tabs

    def on_menu_file_quit(self, widget):
        if not self.delete_event(None, None):
            self.destroy(None)

    def on_menu_edit_vocab(self, widget):
        print "on_menu_edit_vocab"

        dialog = DialogVocabListEditor(self)
        result = dialog.run()
        dialog.destroy()

        if result == gtk.RESPONSE_OK:
            print "OK was clicked."
            # If OK was pressed, update the WordDict GUI's current/max index.
        else:
            print "Cancel was clicked; dialog input discarded."

    def on_menu_edit_kanji(self, widget):
        print "on_menu_edit_kanji"

        dialog = DialogKanjiListEditor(self)
        result = dialog.run()
        dialog.destroy()

        if result == gtk.RESPONSE_OK:
            print "OK was clicked."
            # If OK was pressed, update the KanjiDict GUI's current/max index.
        else:
            print "Cancel was clicked; dialog input discarded."

    def on_menu_edit_prefs(self, widget):
        print "on_menu_edit_prefs"

        dialog = DialogPreferences(self)
        result = dialog.run()
        dialog.destroy()

        if result == gtk.RESPONSE_OK:
            print "OK was clicked."
        else:
            print "Cancel was clicked; dialog input discarded."

    def on_menu_practice_kanji(self, widget):
        print "on_menu_practice_kanji"
        # Show test choice dialog ("pre-test")
        # If "OK",
        # * clear dictionary panels (no cheating, at least not that easily!)
        # * show main test dialog
        # * show test results dialog ("post-test")
        im = InfoMessage(self, _("Not yet implemented"),
                         _("Sorry, this has not yet been re-implemented."))
        im.run()
        im.destroy()

    def on_menu_tools_hand(self, widget):
        print "on_menu_tools_hand"
        # Show kanji handwriting pad... no real reason to make it modal; allow
        # the user to open multiple ones if they desire.
        hwpad = WindowKanjiHWSearch()

    def on_menu_tools_kanji_search(self, widget):
        print "on_menu_tools_kanji_search"
        im = InfoMessage(self, _("Not yet implemented"),
                         _("Sorry, this has not yet been re-implemented."))
        im.run()
        im.destroy()

    def on_menu_help_about(self, widget):
        message = _(
            "%s %s\n"
            "By %s\n"
            "Copyright %s\n\n"
            "Inspired in large by JWPce and JFC by Glenn Rosenthal:\n"
            "http://www.physics.ucla.edu/~grosenth/\n\n"

            "Powered by the many Japanese dictionary files from Monash "
            "University, many thanks to Jim Breen:\n"
            "http://www.csse.monash.edu.au/~jwb/japanese.html\n"
            "Thanks also to Jim Rose of kanjicafe.com for his extended "
            "RADKFILE2/KRADFILE2 databases and derived database files.\n\n"

            "Built using PyGTK: http://www.pygtk.org/\n\n"

            "Hand writing recognition is based upon code from im-ja "
            "(http://im-ja.sourceforge.net/) and KanjiPad "
            "(http://fishsoup.net/software/kanjipad/).  KanjiPad was "
            "written by Owen Taylor.\n\n"

            "See \"Help->License Information...\" for important license "
            "details."
            ) % (PROGRAM_NAME, VERSION_STR, AUTHOR_NAME, COPYRIGHT_DATE)

        im = InfoMessage(self, _("About %s") % PROGRAM_NAME, message)
        im.run()
        im.destroy()

    def on_menu_help_license(self, widget):
        message = _(
            "Program distributed under the GNU General Public License (GPL) "
            "version 2:\n"
            "http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt\n\n"

            "The included dictionary data files, with the exception of the "
            "handwriting databases and Jim Rose's extensions to the radical "
            "databases, are distributed under a separate license specified "
            "at\n"
            "http://www.csse.monash.edu.au/~jwb/edrdg/license.htm\n\n"

            "Jim Rose's extended databases are licensed to Monash University "
            "with permission to modify and redistribute the files, as long as "
            "his copyright notices are preserved.\n\n"

            "The SKIP (System of Kanji Indexing by Patterns) system for "
            "ordering kanji was developed by Jack Halpern (Kanji Dictionary "
            "Publishing Society at http://www.kanji.org/), and is used with "
            "his permission.\n\n"

            "Copies of the GNU General Public License, Monash University's "
            "license for the dictionary files and documentation for the "
            "dictionary files are contained in this program's \"license\" "
            "directory."
            )

        im = InfoMessage(self, _("License Information"), message)
	im.run()
        im.destroy()
