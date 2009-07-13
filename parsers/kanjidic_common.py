# -*- coding: utf-8 -*-

# Copyright (c) 2009, Paul Goins
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""Helper functions for KANJIDIC and KANJIDIC2 parsers.

This module is not intended to be used by itself.

"""

def jstring_convert(us):
    """Convert's from Jim Breen's -x.xx- notation to 〜x(xx)〜 notation."""
    if us[0] == u'-' or us[-1] == u'-':
        us = us.replace(u'-', u'〜')
    parts = us.split('.', 1)
    if len(parts) == 1: return us
    return u"%s(%s)" % tuple(parts)

def kanjidic2_key_to_str(dkey):
    """Converts KANJIDIC2 dictionary keys to KANJIDIC2.

    If unable to find a KANJIDIC2 key, returns the original key.

    """
    d = {
        "halpern_njecd":
        _(u"New Japanese-English Character Dictionary (Halpern)"),
        "nelson_c":
        _(u"Modern Reader's Japanese-English Character Dictionary (Nelson)"),
        "nelson_n":
        _(u"The New Nelson Japanese-English Character Dictionary (Haig)"),
        "sh_kk": _(u"Kanji and Kana (Spahn/Hadamitzky)"),
        #"moro": "Morohashi Daikanwajiten"  morohashi stuff, ...do later
        "henshall":
        _(u"A Guide To Remembering Japanese Characters (Henshall)"),
        "gakken": _(u"A New Dictionary of Kanji Usage (Gakken)"),
        "heisig": _(u"Remembering the Kanji (Heisig)"),
        "oneill_names": _(u"Japanese Names (O'Neill)"),
        "busy_people": _(u"Japanese For Busy People (AJLT)"),
        "crowley": _(u"The Kanji Way to Japanese Language Power (Crowley)"),
        "jf_cards": _(u"Japanese Kanji Flashcards (Hodges/Okazaki)"),
        "kodansha_compact": _(u"Kodansha Compact Kanji Guide"),
        "henshall3": _(u"A Guide To Reading and Writing Japanese (Henshall)"),
        "kanji_in_context": _(u"Kanji in Context (Nishiguchi/Kono)"),
        "halpern_kkld": _(u"Kodansha Kanji Learners Dictionary (Halpern)"),
        "oneill_kk": _(u"Essential Kanji (O'Neill)"),
        "sakade": _(u"A Guide To Reading and Writing Japanese (Sakade)"),
        "tutt_cards": _(u"Tuttle Kanji Cards (Kask)"),
        "maniette": _(u"French version of Heisig (Maniette)")
        }
    return d.get(dkey, dkey)

def qcode_to_desc(qkey):
    d = {
        u'skip': u'SKIP',
        u'deroo': u'De Roo',
        u'sh_desc': u'Spahn/Hadamitzky Kanji Dictionary',
        u'four_corner': u'Four Corner'
        }
    return d.get(qkey, qkey)
