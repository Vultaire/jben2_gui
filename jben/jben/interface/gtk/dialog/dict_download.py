# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os, Queue, urllib2
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
        self.urls = ["/".join((mirror, f)) for f in files]
        self.handled_urls = []

    def on_show(self, widget):
        self._do_new_thread()

    def run(self):
        """Single-time run command; hides GTK boilerplate."""
        gtk.Dialog.run(self)
        self.destroy()

    def _layout(self):
        self.ok_btn = self.add_button(gtk.STOCK_OK, gtk.RESPONSE_OK)
        self.ok_btn.set_sensitive(False)

    def _do_new_thread(self):
        try:
            url = self.urls.pop()
            print "Starting new thread for download:", url
            fname = url.rsplit('/', 1)[-1]
            out_fname = os.path.join(self.app.dictmgr.get_dict_dir(), fname)
            dt = DownloadThread(url, out_fname, timeout=5)
            dt.start()
            gobject.timeout_add(250, self.on_thread_poll, dt)
        except IndexError:
            print "URL queue empty, finishing up"
            self._finish()

    def on_thread_poll(self, dt):
        try:
            while True:
                (message, status) = dt.out_queue.get(block=False)
                if message == dt.CONNECTING:
                    print "Connecting..."
                elif message == dt.CONNECTED:
                    print "Connected.  Url: %s, file size: %d" % \
                          (dt.realurl, dt.filesize or 0)
                elif message == dt.DOWNLOADING:
                    if dt.filesize:
                        pct = (100 * status / dt.filesize) if status else 0
                        print "Downloading: %d bytes received (%d%%)" % \
                              (status, pct)
                    else:
                        print "Downloading: %d bytes received" % status
                elif message == dt.DONE:
                    print "Download complete."
                    self._do_new_thread()
                    return False
                elif message == dt.ERROR:
                    if type(status) is urllib2.URLError:
                        print "Error opening %s: %s" % \
                              (dt.realurl or dt.url, status.reason)
                    else:
                        print "Error occurred during download:", status
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
