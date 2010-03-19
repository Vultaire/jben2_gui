# -*- coding: utf-8 -*-

"""Module for testing kanjidic2.

Added when testing on Debian Lenny (stable).  The latest Python is
2.5.2, which seems to not run the kanjidic2 console tester due to
relative import problems.

"""

from __future__ import absolute_import

from jbparse.kanjidic2 import Parser, encode_or_else
import os


if __name__ == "__main__":
    import sys, locale
    # This is horrid, but it seems like in Python 2.x there doesn't
    # exist an alternative accepted method that's transparent to the
    # typical end user...
    reload(sys)
    sys.setdefaultencoding(locale.getpreferredencoding())

    try:
        dfname, args = sys.argv[1], sys.argv[2:]
        assert args
    except (IndexError, AssertionError):
        print _(u"Syntax: %s <dict_file> <character [...]>") % sys.argv[0]
        exit(-1)

    try:
        p = Parser(dfname)
    except Exception, e:
        print _(u"Could not create Kanjidic2Parser: %s") % unicode(e)
        exit(-1)

    if os.name == "nt":
        charset = "cp932"
    else:
        charset = "utf-8"

    print u"HEADER"
    print u"======"
    print p.get_header()
    print
    print u"%d characters found" % len(p.characters)

    for i, kanji in enumerate(p.search("".join(args).decode(charset))):
        kstr = encode_or_else(unicode(kanji))
        print _(u"Entry %d:\n%s\n") % (i+1, kstr)
