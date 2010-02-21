# -*- coding: utf-8 -*-

from __future__ import with_statement

import threading, Queue, urllib2
import sys


class DownloadThread(threading.Thread):

    """Thread object for downloading files.

    Takes a url string and output file name as required parameters.

    This object communicates via two Queues.  in_queue takes messages
    from other threads, while out_queue reports this thread's status
    to external observers.

    *Please note that in_queue takes single items in, while out_queue
    takes two item tuples.*

    in_queue supports the following messages:

    - ABORT: tells the download thread to gracefully terminate at the
      next available opportunity.

    out_queue supports the following messages:

    - CONNECTING: Sent just before the thread calls urllib2 to
      establish a connection.  Sent as the two-item tuple (CONNECTING,
      0).

    - CONNECTED: Sent once a connection has been established and
      header info has been retrieved.  Sent as the tuple (CONNECTED,
      <content-length>).  If no content-length header was observed, it
      will be sent as (CONNECTED, 0).

    - DOWNLOADING: Sent at each iteration through the download loop.
      Sent as (DOWNLOADING, <progress>), where progress is how many
      bytes have been received so far.

    - DONE: Sent when the download loop finishes successfully.  Sent
      as (DONE, <progress>), where progress is how many bytes were
      received.  This could be double-checked against the
      content-length parameter if desired.

    - ERROR: Sent if an exception occurs.  Sent as (ERROR,
      <exception>), where exception is the exception object caught.

    Additionally, the following parameters are safe to be read from
    other threads:

    realurl: Set while connecting.  After the CONNECTED message is
    received, this should contain the real URL retrieved, in case a
    redirect occurred.

    filesize: Also set while connecting.  After CONNECTED is received,
    this should have the file's file size.  Note that not all requests
    will contain this information, but for general download content it
    should usually work.

    """

    # out_queue messages
    CONNECTING, CONNECTED, DOWNLOADING, DONE, ERROR = range(5)
    # in_queue messages
    ABORT = 1

    def __init__(self, url, fname, chunk_size=16384, timeout=None):
        threading.Thread.__init__(self)
        self.out_queue = Queue.Queue(0)
        self.in_queue = Queue.Queue(0)
        self.url = url
        self.realurl = None
        self.filesize = None
        self.fname = fname
        self.chunk_size = chunk_size
        self.timeout = timeout

    def run(self):
        try:
            with open(self.fname, "wb") as ofile:
                progress = 0
                self.out_queue.put((self.CONNECTING, 0))
                if not (self.timeout is None):
                    resp = urllib2.urlopen(self.url, timeout=self.timeout)
                else:
                    resp = urllib2.urlopen(self.url)
                self.realurl = resp.geturl()
                info = resp.info()
                size_headers = info.getheaders("content-length")
                self.file_size = int(size_headers[0]) if size_headers else None
                self.out_queue.put((self.CONNECTED, self.file_size))
                while True:
                    try:
                        event = self.in_queue.get(block=False)
                    except Queue.Empty:
                        event = None
                    if event == self.ABORT:
                        raise Exception("Aborted by parent thread")
                    self.out_queue.put((self.DOWNLOADING, progress))
                    d = resp.read(self.chunk_size)
                    if not d:
                        break
                    ofile.write(d)
                    progress += len(d)
                self.out_queue.put((self.DONE, progress))
        except Exception, e:
            self.out_queue.put((self.ERROR, e))


# This module can be executed independently via:
#   python -m jben.download_thread <url> <outfile>

def main():
    assert len(sys.argv) >= 2, "Please specify a URL to download."
    assert len(sys.argv) >= 3, "Please specify a file name to save to."
    dt = DownloadThread(sys.argv[1], sys.argv[2], timeout=5)
    print "Starting thread..."
    dt.start()
    try:
        fsize = None
        while True:
            (status, progress) = dt.out_queue.get(block=True)
            if status == dt.CONNECTING:
                print "Connecting..."
            elif status == dt.CONNECTED:
                fsize = progress
                if fsize:
                    print "Connected; file size: %d" % fsize
                else:
                    print "Connected; unknown file size"
            elif status == dt.DOWNLOADING:
                if fsize:
                    pct = (100 * progress / fsize) if progress else 0
                    print "Downloading: %d bytes received (%d%%)" % \
                          (progress, pct)
                else:
                    print "Downloading: %d bytes received" % progress
            elif status == dt.DONE:
                break
            elif status == dt.ERROR:
                # progress is an exception object
                raise progress
    except KeyboardInterrupt, e:
        print "Keyboard interrupt received; aborting."
        dt.in_queue.put(dt.ABORT)
    dt.join()
    if fsize:
        pct = (100 * progress / fsize) if progress else 0
        print "Done!  %d of %d bytes received! (%d%%)" % (progress, fsize, pct)
    else:
        print "Done!  %d bytes received!" % progress

if __name__ == "__main__":
    main()
