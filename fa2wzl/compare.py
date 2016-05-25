import difflib

from fa2wzl.logging import logger


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


def convert_submission_category(cat_str):
    """Return a Weasyl subcategory ID for a given string category name.

    Args:
        cat_str (str): The category name

    Returns:
        int: The integer category ID

    Raises:
        KeyError: If there is no appropriate mapping
    """
    mapping = {
        "Artwork (Digital)": 1030,
        "Artwork (Traditional)": 1020,
        "Cellshading": 1030,
        "Crafting": 1075,
        "Designs": 1060,
        "Flash": 1040,
        "Fursuiting": 1050,
        "Icons": 1999,
        "Mosaics": 1999,
        "Photography": 1050,
        "Sculpting": 1070,

        "Story": 2010,
        "Poetry": 2020,
        "Prose": 2999,

        "Music": 3999,
        "Podcasts": 3040,

        "Desktops": 1080,
        "Wallpaper": 1080,
        "Screenshots": 1999,
    }

    return mapping[cat_str]


def convert_rating(rating_str):
    """Convert a FA rating string to a Weasyl rating.

    Args:
        rating_str (str): The rating name

    Returns:
        int: The rating value

    Raises:
        KeyError: If no appropriate rating is found
    """
    mapping = {
        "general": 10,
        "mature": 30,
        "adult": 40,
    }

    return mapping[rating_str]


def map_folders(fa_folders, wzl_folders):
    mapped = match_objects(wzl_folders, lambda x: x.title, fa_folders,
                           lambda x: x.title)

    mapped = list(mapped)

    for wzl_folder, fa_folder in mapped:
        sub_mapped = match_objects(wzl_folder.children, lambda x: x.title,
                                   fa_folder.children, lambda x: x.title)

        mapped.extend(list(sub_mapped))

    return [(m[1], m[0]) for m in mapped]


def get_unmapped_folders(fa_folders, mapping):
    unmapped_folders = set()

    for folder in fa_folders:
        unmapped_folders.add(folder)

        for subfolder in folder.children:
            unmapped_folders.add(subfolder)

    unmapped_folders -= {fa_folder for fa_folder, wzl_folder in mapping}

    return unmapped_folders


def create_unmapped_folders(fa_sess, wzl_sess, unmapped_folders):
    for folder in fa_sess.folders:
        if folder in unmapped_folders:
            new_wzl_folder = wzl_sess.create_folder(folder.title)

            for subfolder in folder.children:
                if subfolder in unmapped_folders:
                    wzl_sess.create_folder(subfolder.title, new_wzl_folder.id)
