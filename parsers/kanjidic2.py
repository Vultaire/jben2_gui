#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import gettext
#gettext.install('pyjben', unicode=True)

def kanjidic2_key_to_str(dkey):
    """Converts KANJIDIC2 dictionary keys to KANJIDIC2.

    If unable to find a KANJIDIC2 key, returns the original key.

    """
    d = {
        "halpern_njecd": _("New Japanese-English Character Dictionary (Halpern)"),
        "nelson_c": _("Modern Reader's Japanese-English Character Dictionary (Nelson)"),
        "nelson_n": _("The New Nelson Japanese-English Character Dictionary (Haig)"),
        "sh_kk": _("Kanji and Kana (Spahn/Hadamitzky)"),
        #"moro": "Morohashi Daikanwajiten"  morohashi stuff, ...do later
        "henshall": _("A Guide To Remembering Japanese Characters (Henshall)"),
        "gakken": _("A New Dictionary of Kanji Usage (Gakken)"),
        "heisig": _("Remembering the Kanji (Heisig)"),
        "oneill_names": _("Japanese Names (O'Neill)"),
        "busy_people": _("Japanese For Busy People (AJLT)"),
        "crowley": _("The Kanji Way to Japanese Language Power (Crowley)"),
        "jf_cards": _("Japanese Kanji Flashcards (Hodges/Okazaki)"),
        "kodansha_compact": _("Kodansha Compact Kanji Guide"),
        "henshall3": _("A Guide To Reading and Writing Japanese (Henshall)"),
        "kanji_in_context": _("Kanji in Context (Nishiguchi/Kono)"),
        "halpern_kkld": _("Kodansha Kanji Learners Dictionary (Halpern)"),
        "oneill_kk": _("Essential Kanji (O'Neill)"),
        "sakade": _("A Guide To Reading and Writing Japanese (Sakade)"),
        "tutt_cards": _("Tuttle Kanji Cards (Kask)"),
        "maniette": _("French version of Heisig (Maniette)")
        }
    return d.get(dkey, dkey)
