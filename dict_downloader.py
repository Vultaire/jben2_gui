# -*- coding: utf-8 -*-

import urllib2

# The following is shamelessly copied from:
# http://ftp.monash.edu.au/pub/nihongo/.message
static_mirror_list = [
    "http://ftp.monash.edu.au/pub/nihongo", # Original FTP archive
    "http://japanology.arts.kuleuven.ac.be/mirrors/monash", # Belgium
    "ftp://ftp.nrc.ca/pub/packages/nihongo", # Canada (fast site)
    "http://www.bcit-broadcast.com/monash", # Canada (http only)
    "ftp://ftp.sedl.org/pub/mirrors/nihongo", # US(Texas)
    "ftp://ftp.net.usf.edu/pub/monash", # IS (Florida)
    "ftp://ftp.u-aizu.ac.jp/pub/SciEng/nihongo/ftp.cc.monash.edu.au", # Japan
    "ftp://ftp.funet.fi/pub/culture/japan/mirrors/monash", # Finland
    "ftp://ftp.uni-duisburg.de/Mirrors/ftp.monash.edu.au/pub/nihongo" # Germany
    ]

def get_mirror_list(from_inet=None,
                    mirror="http://ftp.monash.edu.au/pub/nihongo"):
    """Grabs a mirror list from a valid mirror of Jim Breen's FTP archive."""
    # First, try to grab from the internet.
    if from_inet in (None, True):
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
            pass
    if from_inet in (None, False):
        return static_mirror_list
    return []

def get_dict(mirror_url, dict_name):
    try:
        url = "%s/%s" % (mirror_url, dict_name)
        f = urllib2.urlopen(url)
        return f or None
    except urllib2.URLError, e:
        return None

def console_install():
    import sys

    # Should default to something like $HOME/.jben.d/dicts for single
    # user install, or ../share/jben/dicts for all user install.
    # ... "All user install" will initially NOT be supported, but will
    # be later.
    dpath = p.get_dict_path()
    #print "Using output dict path:", dpath

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

    urls = []
    for d in s.split():
        try:
            i = int(d) - 1
            if i not in range(len(dicts)):
                continue
            fname = dicts[i][0]
            mirror = get_mirror_list(from_inet=False)[0]
            url = "%s/%s" % (mirror, fname)
            urls.append([fname, url])
        except ValueError:
            pass

    for fname, url in urls:
        target_fname = "%s/%s" % (dpath, fname)
        print "SIMULATION: Downloading %s to %s..." % (url, target_fname)

if __name__ == "__main__":
    import preferences as p
    p.load()
    console_install()
