# -*- coding: utf-8 -*-

from __future__ import absolute_import

import sys, os, Queue, urllib2
import gtk, gobject
from ..widget.storedsize import StoredSizeDialog
from jben.download_thread import DownloadThread


class DictDownload(StoredSizeDialog):

    """Downloads dictionaries from a specified mirror."""

    def __init__(self, app, parent, mirror, files):
        StoredSizeDialog.__init__(
            self, "gui.dialog.dict_download.size", -1, -1,
            title=_("Download dictionaries"),
            parent=parent,
            flags=gtk.DIALOG_MODAL
            )
        self.app = app
        self._layout()
        self.connect("show", self.on_show)
        self.connect("destroy", self.on_destroy)
        self.urls = ["/".join((mirror, f)) for f in files]
        self.handled_urls = []
        self.dt = None
        self.timeout_src = None

    def on_show(self, widget):
        self._do_new_thread()

    def on_destroy(self, widget):
        print "on_destroy called"
        self.set_sensitive(False)
        if self.timeout_src:
            if not gobject.source_remove(self.timeout_src):
                print >> sys.stderr, "WARNING: Could not remove timeout"
        if self.dt:
            self.dt.abort()
            self.dt.join()

    def run(self):
        """Single-time run command; hides GTK boilerplate."""
        gtk.Dialog.run(self)
        self.destroy()

    def _layout(self):
        self.ok_btn = self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.ok_btn.set_sensitive(False)

    def _add_progress_bar(self):
        layout = self.get_content_area()
        self.cur_prog_bar = gtk.ProgressBar()
        self.cur_prog_bar.set_pulse_step(0.01)
        layout.pack_start(self.cur_prog_bar, expand=False)
        layout.show_all()

    def _do_new_thread(self):
        try:
            url = self.urls.pop()
            print "Starting new thread for download:", url
            fname = url.rsplit('/', 1)[-1]
            out_fname = os.path.join(
                self.app.dictmgr.get_writeable_dict_directory(), fname)
            self.dt = DownloadThread(url, out_fname, timeout=5)
            self.dt.start()
            self._add_progress_bar()
            self.timeout_src = gobject.timeout_add(10, self.on_thread_poll,
                                                   self.dt)
        except IndexError:
            print "URL queue empty, finishing up"
            self._finish()

    def on_thread_poll(self, dt):
        try:
            while True:
                (message, status) = dt.out_queue.get(block=False)
                if message == dt.CONNECTING:
                    self.cur_prog_bar.set_text("Connecting...")
                elif message == dt.CONNECTED:
                    self.cur_prog_bar.set_text(dt.realurl)
                elif message == dt.DOWNLOADING:
                    if dt.filesize:
                        frct = status / float(dt.filesize)
                        pct = (100 * frct) if status else 0
                        out_str = "%s: %d bytes (%f)%%" % (
                            dt.realurl, status, pct)
                        self.cur_prog_bar.set_text(out_str)
                        self.cur_prog_bar.set_fraction(max(frct, 1.0))
                    else:
                        out_str = "%s: %d bytes" % (dt.realurl, status)
                        self.cur_prog_bar.set_text(out_str)
                        self.cur_prog_bar.pulse()
                elif message == dt.DONE:
                    self.cur_prog_bar.set_text("Download complete")
                    self.cur_prog_bar.set_fraction(1.0)
                    self._do_new_thread()
                    return False
                elif message == dt.ERROR:
                    if type(status) is urllib2.URLError:
                        err_str = "Error opening %s: %s" % \
                                  (dt.realurl or dt.url, status.reason)
                    else:
                        err_str = "Error occurred during download: %s" % \
                                  str(status)
                    self.cur_prog_bar.set_text(err_str)
                    self._do_new_thread()
                    return False
                else:
                    raise Exception("Unknown thread message: (%s, %s)" %
                                    (message, status))
        except Queue.Empty:
            return True

    def _thread_finished(self, thread):
        self.handled_urls.append(thread.realurl)
        self._do_new_thread()

    def _finish(self):
        self.ok_btn.set_sensitive(True)
