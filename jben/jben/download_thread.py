# -*- coding: utf-8 -*-

from __future__ import with_statement

import threading, Queue, urllib2
import sys


class DownloadThread(threading.Thread):

    """Thread object for downloading files.

    Takes a url string and output file name as required parameters.

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
                # ****************
                info = resp.info()
                size_headers = info.getheaders("content-length")
                file_size = size_headers[0] if size_headers else None
                print "FILE SIZE for %s:" % self.url, file_size
                self.out_queue.put((self.CONNECTED, file_size))
                # ****************
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


def main():
    assert len(sys.argv) >= 2, "Please specify a URL to download."
    assert len(sys.argv) >= 3, "Please specify a file name to save to."
    dt = DownloadThread(sys.argv[1], sys.argv[2], timeout=5)
    print "Starting thread..."
    dt.start()
    try:
        while True:
            (status, progress) = dt.out_queue.get(block=True)
            if status == dt.CONNECTING:
                print "Connecting..."
            elif status == dt.DOWNLOADING:
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
    print "Done!  %d bytes received!" % progress

if __name__ == "__main__":
    main()
