# -*- coding: utf-8 -*-

from __future__ import absolute_import

import urllib2, sys, os, random
from jben.preferences import Preferences
from jben.dict import DictManager

# The following is shamelessly copied from:
# http://ftp.monash.edu.au/pub/nihongo/.message
#old_static_mirror_list = [
#    "http://ftp.monash.edu.au/pub/nihongo", # Original FTP archive
#    "http://japanology.arts.kuleuven.ac.be/mirrors/monash", # Belgium
#    "ftp://ftp.nrc.ca/pub/packages/nihongo", # Canada (fast site)
#    "http://www.bcit-broadcast.com/monash", # Canada (http only)
#    "ftp://ftp.sedl.org/pub/mirrors/nihongo", # US(Texas)
#    "ftp://ftp.net.usf.edu/pub/monash", # IS (Florida)
#    "ftp://ftp.u-aizu.ac.jp/pub/SciEng/nihongo/ftp.cc.monash.edu.au", # Japan
#    "ftp://ftp.funet.fi/pub/culture/japan/mirrors/monash", # Finland
#    "ftp://ftp.uni-duisburg.de/Mirrors/ftp.monash.edu.au/pub/nihongo" # Germany
#    ]

# Based upon checking the mirrors myself, this is the list I'll use
# for J-Ben.
static_mirror_list = [
    # Official archive
    # (redirects to ringtail.its.monash.edu.au/pub/nihongo, same IP address)
    "http://ftp.monash.edu.au/pub/nihongo",
    # Up to date mirrors
    "ftp://ftp.nrc.ca/pub/packages/nihongo", # Canada (fast site)
    "ftp://ftp.net.usf.edu/pub/monash/pub/nihongo", # IS (Florida)
    "ftp://ftp.uni-duisburg.de/Mirrors/ftp.monash.edu.au/pub/nihongo", # Germany
    # *Probably* up to date (but can't tell since I can't see file mtimes)
    "http://japanology.arts.kuleuven.ac.be/mirrors/monash", # Belgium
    "http://www.bcit-broadcast.com/monash", # Canada (http only)
    # old links
    #"ftp://ftp.u-aizu.ac.jp/pub/SciEng/nihongo/ftp.cc.monash.edu.au", # Japan
    #"ftp://ftp.funet.fi/pub/culture/japan/mirrors/monash", # Finland
    # bad links
    #"ftp://ftp.sedl.org/pub/mirrors/nihongo", # US(Texas)  - "not available"
    ]

def get_mirror_list(from_inet=False,
                    mirror="http://ftp.monash.edu.au/pub/nihongo"):
    """Grabs a mirror list from a valid mirror of Jim Breen's FTP archive."""

    # NOTE: although this function does what it says, the mirror list
    # is not dependable for our purposes.  Not all mirrors are up to
    # date, and one mirror appears to be down.  I advise not using
    # from_inet for the time being.

    if from_inet:
        try:
            f = urllib2.urlopen("%s/%s" % (mirror, ".message"))
            if f:
                mirrors = ["http://ftp.monash.edu.au/pub/nihongo"]
                for line in f:
                    if line[0] == ".":
                        line = line[1:].strip().replace("\t", " ")
                        l = [s.strip() for s in line.split(" ", 1)]
                        url, desc = l
                        url = url.rstrip('/')
                        mirrors.append(url)
                return mirrors
        except urllib2.URLError, e:
            print >> sys.stderr, e
            pass

        return []
    else:
        return static_mirror_list

def download_dict(fname):
    mirrors = get_mirror_list(from_inet=False)

    dpath = DictManager.get_writeable_dict_directory()

    def get_next_mirror():
        i = random.randrange(0, len(mirrors))
        return mirrors.pop(i)

    mirror = get_next_mirror()

    while True:
        url = "%s/%s" % (mirror, fname)
        target_fname = "%s/%s" % (dpath, fname)
        try:
            #print "Downloading %s to %s..." % (url, target_fname)
            resp = urllib2.urlopen(url)
            data = resp.read()
            resp.close()
            if not os.path.exists(dpath):
                os.mkdir(dpath)
            ofile = open(target_fname, "wb")
            ofile.write(data)
            ofile.close()
            break
        except Exception, e:
            print >> sys.stderr, \
                  "An error occurred; trying the next mirror."
            print >> sys.stderr, "(%s)" % str(e)
            mirror = get_next_mirror()


def console_iface():
    p = Preferences()
    p.load()

    print "The following dictionaries are available:"
    dicts = [("edict.gz", "EDICT"),
             #("edict2.gz", "EDICT2"),
             ("JMdict.gz", "JMdict (full)"),
             ("JMdict_e.gz", "JMdict_e (English only)"),
             ("kanjidic.gz", "KANJIDIC"),
             #("kanjd212.gz", "KANJD212"),
             ("kanjidic2.xml.gz", "KANJIDIC2")]
    for i, (fname, desc) in enumerate(dicts):
        print "\t%d: %s" % (i+1, desc)
    sys.stdout.write("Enter the numbers for the dictionaries you want, "
                     "separated by spaces: ")
    s = sys.stdin.readline()

    fnames = []
    for d in s.split():
        try:
            i = int(d) - 1
            if i not in range(len(dicts)):
                print >> sys.stderr, "Value %s is out of range." % s
                continue
        except ValueError, e:
            print >> sys.stderr, "Ignoring invalid value %s" % d
            continue
        fname = dicts[i][0]
        fnames.append(fname)

    for fname in fnames:
        download_dict(fname)

if __name__ == "__main__":
    console_iface()
