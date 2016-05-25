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


def compute_folder_tasks(fa_folders, wzl_folders):
    matches = list(match_objects(fa_folders, lambda x: x.title, wzl_folders,
                                 lambda x: x.title))
    unmatched_fa_folders = set(fa_folders) - {m[0] for m in matches}

    return set(unmatched_fa_folders)


def create_wzl_folders(fa_sess, wzl_sess, new_folders):
    # Create root folders first
    logger.debug("Creating root folders")
    for folder in fa_sess.folders:
        if folder in new_folders:
            wzl_sess.create_folder(folder.title)

    # Reload
    wzl_sess.reload_folders()

    # Create child folders
    logger.debug("Creating child folders")
    for folder in fa_sess.folders:
        for subfolder in folder.children:
            if subfolder in new_folders:

                # Find created folder by title
                # TODO: kind of hacky, try to determine the new folder id when
                # creating it instead and work off of that

                parent_id = 0

                for wzl_parent_folder in wzl_sess._folders.values():
                    if wzl_parent_folder.title == folder.title:
                        parent_id = wzl_parent_folder.id
                        break

                wzl_sess.create_folder(subfolder.title, parent_id)

    # Reload once more
    wzl_sess.reload_folders()
