# -*- coding: utf-8 -*-

import threading, Queue, urllib2
import sys


class DownloadThread(threading.Thread):

    CONNECTING, DOWNLOADING, DONE, ERROR = range(4)
    ABORT = 1

    def __init__(self, url, chunk_size=16384, timeout=None):
        threading.Thread.__init__(self)
        self.out_queue = Queue.Queue(0)
        self.in_queue = Queue.Queue(0)
        self.url = url
        self.chunk_size = chunk_size
        self.timeout = timeout

    def run(self):
        try:
            data = []
            progress = 0
            self.out_queue.put((0, self.CONNECTING))
            if not (self.timeout is None):
                resp = urllib2.urlopen(self.url, timeout=self.timeout)
            else:
                resp = urllib2.urlopen(self.url)
            while True:
                try:
                    event = self.in_queue.get(block=False)
                except Queue.Empty:
                    event = None
                if event == self.ABORT:
                    raise Exception("Aborted by parent thread")
                self.out_queue.put((progress, self.DOWNLOADING))
                d = resp.read(self.chunk_size)
                if not d:
                    break
                progress += len(d)
            self.out_queue.put((progress, self.DONE))
        except Exception, e:
            self.out_queue.put((e, self.ERROR))


def main():
    assert len(sys.argv) == 2, "Please specify a URL to download."
    dt = DownloadThread(sys.argv[1], timeout=5)
    print "Starting thread..."
    dt.start()
    try:
        while True:
            (progress, status) = dt.out_queue.get(block=True)
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
