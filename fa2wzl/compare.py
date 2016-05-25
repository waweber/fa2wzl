import difflib


def match_objects(subjects, subj_key, possible_matches, match_key):
    """Get pairs of objects that are probably the same.

    Args:
        subjects: The list of things to match
        subj_key: Callable that returns the item to compare with for each
            subject
        possible_matches: The list of things to match from
        match_key: Callable that returns the item to compare with for each
            possible match

    Yields:
        Pairs of objects from subjects and possible_matches
    """
    if len(subjects) == 0 or len(possible_matches) == 0:
        return

    equivs = {}

    for subject in subjects:
        scores = []

        for match in possible_matches:
            ratio = difflib.SequenceMatcher(a=subj_key(subject),
                                            b=match_key(match)).ratio()
            scores.append((match, ratio))

        scores.sort(key=lambda x: x[1], reverse=True)

        best_match, best_score = scores[0]

        if best_score >= 0.7:
            equivs[best_match] = subject, best_score

    for match, (subject, score) in equivs.items():
        yield subject, match
