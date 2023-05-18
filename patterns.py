# Rule-based matching patterns for consice (business) writing.

pattern_descriptions = {
    "ambiguousOpenings": (
        "A pronoun followed by a 'to be' verb is a vague sentence opening, try"
        " to be specific."
    ),
    "ambiguousPronouns": (
        "Ambiguous pronouns are vague, the more precise your writing, the"
        " better."
    ),
    "lyAdverbs": (
        "Adverbs that end with 'ly' can *usually* be removed from your"
        " document without losing meaning."
    ),
    "passiveVoice": (
        "A 'to be' verb followed by another verb is an indicator of passive"
        " voice. Try to write >= 90% of your document in active voice."
    ),
}

ambiguous_openings = [
    {"TEXT": {"IN": ["It", "That", "There", "These", "Those", "This"]}},
    {"LEMMA": "be"},
]
ambiguous_pronouns = [
    {"TEXT": {"IN": ["it", "that", "there", "these", "those", "this"]}}
]
ly_adverbs = [{"TEXT": {"REGEX": r"\w+ly$"}}]
passive_voice = [{"LEMMA": "be"}, {"POS": "VERB"}]
