import difflib


def match_submissions(subjects, possible_matches):
    """Get pairs of submissions that are probably the same submission.

    Args:
        subjects: The list of submissions to match
        possible_matches: The list of submissions to match from

    Yields:
        Pairs of submissions from subjects and possible_matches
    """
    if len(subjects) == 0 or len(possible_matches) == 0:
        return

    equivs = {}

    for subject in subjects:
        scores = []

        for match in possible_matches:
            ratio = difflib.SequenceMatcher(a=subject.title,
                                            b=match.title).ratio()
            scores.append((match, ratio))

        scores.sort(key=lambda x: x[1], reverse=True)

        best_match, best_score = scores[0]
        equivs[best_match] = subject, best_score

    for match, (subject, score) in equivs.items():
        yield subject, match
