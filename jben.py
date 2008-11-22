#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: jben.py
# Author: Paul Goins
# Created on: 20 Nov 2008

import gettext
gettext.install("jben")

import pygtk
pygtk.require("2.0")
import gtk

import tab_worddict
import tab_kanjidict

# These were "constants" under the C++ interface.
# However, since J-Ben has an alternate Japanese name (Ｊ勉),
# and since my name can be written in katakana, or the copyright
# date written in other numbering systems (heisei-based, etc.),
# I'm now using gettext on these "constants".
PROGRAM_NAME = _("J-Ben/python")
AUTHOR_NAME = _("Paul Goins")
COPYRIGHT_DATE = _("2007, 2008")

VERSION_STR = "1.2.1"

def setup_global_icons():
    icon1 = gtk.gdk.pixbuf_new_from_file("jben.xpm")
    icon2 = gtk.gdk.pixbuf_new_from_file("jben_48.xpm")
    icon3 = gtk.gdk.pixbuf_new_from_file("jben_32.xpm")
    icon4 = gtk.gdk.pixbuf_new_from_file("jben_16.xpm")
    gtk.window_set_default_icon_list(icon1, icon2, icon3, icon4)

class JBen:
    """The main GUI of J-Ben.  Execute the "main" method to run the program."""

    def delete_event(self, widget, event, data = None):
        return False

    def destroy(self, widget, data = None):
        gtk.main_quit()

    def __init__(self):
        setup_global_icons()

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_title(PROGRAM_NAME)

        self.menu = self.create_menu()
        self.children = self.create_children()

        layout = gtk.VBox(spacing = 5)
        layout.pack_start(self.menu, expand = False)
        layout.pack_start(self.children)

        self.window.add(layout)
        self.window.show_all()

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
        self.window.add_accel_group(uim.get_accel_group())
        return uim.get_widget("/MenuBar")

    def create_children(self):
        tabs = gtk.Notebook()
        worddict = tab_worddict.TabWordDict()
        kanjidict = tab_kanjidict.TabKanjiDict()
        tabs.append_page(worddict.contents,
                              gtk.Label(_("Word Dictionary")))
        tabs.append_page(kanjidict.contents,
                              gtk.Label(_("Kanji Dictionary")))
        return tabs

    def main(self):
        gtk.main()

    def on_menu_file_quit(self, widget):
        self.window.destroy()

    def on_menu_edit_vocab(self, widget):
        print "on_menu_edit_vocab"
        # Create/show vocab list editor
        # If OK was pressed, update the WordDict GUI's current/max index.

    def on_menu_edit_kanji(self, widget):
        print "on_menu_edit_kanji"
        # Create/show kanji list editor
        # If OK was pressed, update the KanjiDict GUI's current/max index.

    def on_menu_edit_prefs(self, widget):
        print "on_menu_edit_prefs"
        # Create/show preferences dialog
        # If OK was pressed, update necessary fields.
        # What to update:
        # * Current dictionary tab
        #   ...but is it really needed?  Maybe the user can just re-search?
        #   Does it confuse the user to change stuff automatically like this?
        # C++ code: (GTK::MainGui.)Update();

    def on_menu_practice_kanji(self, widget):
        print "on_menu_practice_kanji"
        # Show test choice dialog ("pre-test")
        # If "OK",
        # * clear dictionary panels (no cheating, at least not that easily!)
        # * show main test dialog
        # * show test results dialog ("post-test")

    def on_menu_tools_hand(self, widget):
        print "on_menu_tools_hand"
        # Show kanji handwriting pad... no real reason to make it modal; allow
        # the user to open multiple ones if they desire.

    def on_menu_tools_kanji_search(self, widget):
        print "on_menu_tools_kanji_search"
        # Show kanji search dialog... Again, not modal.

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

        md = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,
                               gtk.BUTTONS_OK, message)
        md.set_title(_("About %s") % PROGRAM_NAME)
        md.run()
        md.destroy()

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

        md = gtk.MessageDialog(self.window, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO,
                               gtk.BUTTONS_OK, message)
	md.set_title(_("License Information"))
	md.run()
        md.destroy()

if __name__ == "__main__":
    gui = JBen()
    gui.main()
