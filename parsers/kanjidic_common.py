# -*- coding: utf-8 -*-

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
