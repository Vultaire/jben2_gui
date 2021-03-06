#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Project: J-Ben, Python front-end
# File: window_kanjihwsearch.py
# Author: Paul Goins
# Created on: 25 Nov 2008

from __future__ import absolute_import

import gtk

from jben import jben_globals, configure
from .kanjihwsearch import WindowKanjiHWSearch
from ..widget.worddict import TabWordDict
from ..widget.kanjidict import TabKanjiDict
from ..widget.storedsize import StoredSizeWindow
from ..widget.infomessage import show_message
from ..widget.yesnodialog import show_message_yn
from ..dialog.vocablisteditor import DialogVocabListEditor
from ..dialog.kanjilisteditor import DialogKanjiListEditor
from ..dialog.preferences import DialogPreferences
from ..dialog.dict_mirror_select import DictMirrorSelect
from ..dialog.dict_download import DictDownload


class Main(StoredSizeWindow):
    """The main GUI of J-Ben."""

    def __init__(self, app, param="gui.main.size"):
        StoredSizeWindow.__init__(self, param, 600, 400, gtk.WINDOW_TOPLEVEL)
        self.app = app
        self.connect("show", self.on_show)
        self.connect("destroy", self.on_destroy)
        self._layout_window()

    def on_show(self, widget):
        dictmgr = self.app.dictmgr
        if not dictmgr.all_dicts_found():
            # Ask if we should download dictionaries from the internet.
            downloaded = False
            do_download = show_message_yn(
                self, _("Dictionaries not found"),
                _("Could not find some needed dictionary files.  "
                  "Do you wish to download them from the Internet?"),
                default_button="yes")
            if do_download:
                # Code is a little unclear here...
                mirror = DictMirrorSelect(self.app, self).run()
                if mirror != None:
                    files = dictmgr.get_needed_dict_names()
                    DictDownload(self.app, self, mirror, files).run()
                    downloaded = True
                # Post-DL...
                dictmgr.find_databases()  # try to reload DBs
                if not dictmgr.all_dicts_found():
                    show_message(
                        self, _("Could not download all dictionaries"),
                        _("Could not download all needed files.  "
                          "Some features may be disabled."))
            else:
                show_message(self, _("Not downloading dictionaries"),
                             _("Not downloading dictionaries.  "
                               "Some features may be disabled."))
        if dictmgr.jmdict_found():
            self.worddict.set_dict(dictmgr.jmdict)
            self.worddict.set_sensitive(True)
        if dictmgr.kd2_found():
            self.kanjidict.set_dict(dictmgr.kd2)
            self.kanjidict.set_sensitive(True)
        self.set_sensitive(True)

    def on_destroy(self, widget):
        gtk.main_quit()

    def on_menu_file_quit(self, widget):
        if not self.delete_event(None, None):
            self.destroy()

    def on_menu_edit_vocab(self, widget):
        dialog = DialogVocabListEditor(self)
        result = dialog.run()
        dialog.destroy()

        if result == gtk.RESPONSE_OK:
            # If OK was pressed, update the WordDict GUI's current/max index.
            pass

    def on_menu_edit_kanji(self, widget):
        dialog = DialogKanjiListEditor(self)
        result = dialog.run()
        dialog.destroy()

        if result == gtk.RESPONSE_OK:
            # If OK was pressed, update the KanjiDict GUI's current/max index.
            pass

    def on_menu_edit_prefs(self, widget):
        dialog = DialogPreferences(self)
        result = dialog.run()
        dialog.destroy()

        if result == gtk.RESPONSE_OK:
            # If OK was pressed, refresh the UI.
            pass

    def on_menu_practice_kanji(self, widget):
        print "on_menu_practice_kanji"
        # Show test choice dialog ("pre-test")
        # If "OK",
        # * clear dictionary panels (no cheating, at least not that easily!)
        # * show main test dialog
        # * show test results dialog ("post-test")
        show_message(self, _("Not yet implemented"),
                     _("Sorry, this has not yet been re-implemented."))

    def on_menu_tools_hand(self, widget):
        # Show kanji handwriting pad... no real reason to make it modal; allow
        # the user to open multiple ones if they desire.
        hwpad = WindowKanjiHWSearch()

    def on_menu_tools_kanji_search(self, widget):
        print "on_menu_tools_kanji_search"
        show_message(self, _("Not yet implemented"),
                     _("Sorry, this has not yet been re-implemented."))

    def on_menu_help_about(self, widget):
        message_template = _(
            "%(package_name)s %(package_version)s\n"
            "By %(author)s\n"
            "Copyright %(copyright)s\n\n"
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
            )
        args = {
            "package_name": configure.PACKAGE_NAME,
            "package_version": configure.PACKAGE_VERSION,
            "author": jben_globals.AUTHOR_NAME,
            "copyright": jben_globals.COPYRIGHT_DATE,
            }

        message = message_template % args
        show_message(self, _("About %s") % configure.PACKAGE_NAME, message)

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

        show_message(self, _("License Information"), message)

    def _layout_window(self):
        self.set_title(configure.PACKAGE_NAME)
        self.menu = self._create_menu()
        children = self._create_children()
        layout = gtk.VBox(spacing = 5)
        layout.pack_start(self.menu, expand=False)
        layout.pack_start(children)
        self.add(layout)

    def _create_menu(self):
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

    def _create_children(self):
        tabs = gtk.Notebook()
        self.worddict = TabWordDict()
        self.kanjidict = TabKanjiDict()
        for obj in (self.worddict, self.kanjidict):
            obj.set_sensitive(False)
        tabs.append_page(self.worddict, gtk.Label(_("Word Dictionary")))
        tabs.append_page(self.kanjidict, gtk.Label(_("Kanji Dictionary")))
        return tabs
