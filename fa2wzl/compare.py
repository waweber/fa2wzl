import difflib
from itertools import groupby

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


def convert_submission_type(type_str):
    """Convert a FA type string to a WZL type string.

    Args:
        type_str (str): The FA type string

    Returns:
        str: The weasyl type string

    Raises:
        KeyError: If there is no appropriate type.
    """
    mapping = {
        "image": "visual",
        "text": "literary",
        "audio": "multimedia",
        "flash": "multimedia",
    }

    return mapping[type_str]


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
    """Create a mapping of folders on FA to equivalent ones on Weasyl.

    The folder should be the root folders.

    Args:
        fa_folders: List of FA folders
        wzl_folders: List of WZL folders

    Returns:
        list: A list of pairs of a FA folder and a matched WZL folder.
    """
    mapped = match_objects(wzl_folders, lambda x: x.title, fa_folders,
                           lambda x: x.title)

    mapped = list(mapped)

    for wzl_folder, fa_folder in mapped:
        sub_mapped = match_objects(wzl_folder.children, lambda x: x.title,
                                   fa_folder.children, lambda x: x.title)

        mapped.extend(list(sub_mapped))

    return [(m[1], m[0]) for m in mapped]


def map_submissions(fa_submissions, wzl_submissions):
    """Create a mapping of submissions on FA to equivalent ones on Weasyl.

    Does not consider folders.

    Args:
        fa_submissions: List of all submissions on FA
        wzl_submissions: List of all submissions on WZL
    """

    fa_visual = [s for s in fa_submissions if
                 convert_submission_type(s.type) == "visual"]
    fa_literary = [s for s in fa_submissions if
                   convert_submission_type(s.type) == "literary"]
    fa_multimedia = [s for s in fa_submissions if
                     convert_submission_type(s.type) == "multimedia"]

    wzl_visual = [s for s in wzl_submissions if s.type == "visual"]
    wzl_literary = [s for s in wzl_submissions if s.type == "literary"]
    wzl_multimedia = [s for s in wzl_submissions if s.type == "multimedia"]

    mappings = []

    mappings.extend(match_objects(wzl_visual, lambda x: x.title, fa_visual,
                                  lambda x: x.title))
    mappings.extend(match_objects(wzl_literary, lambda x: x.title, fa_literary,
                                  lambda x: x.title))
    mappings.extend(
        match_objects(wzl_multimedia, lambda x: x.title, fa_multimedia,
                      lambda x: x.title))

    return [(m[1], m[0]) for m in mappings]


def get_unmapped_folders(fa_folders, mapping):
    """Return the FA folders that have not been matched to a WZL folder.

    The folders should be the root folders.

    Args:
        fa_folders: List of FA folders
        mapping: The list of mappings

    Returns:
        set: A set of the folders not found in the mapping
    """
    unmapped_folders = set()

    for folder in fa_folders:
        unmapped_folders.add(folder)

        for subfolder in folder.children:
            unmapped_folders.add(subfolder)

    unmapped_folders -= {fa_folder for fa_folder, wzl_folder in mapping}

    return unmapped_folders


def get_unmapped_submissions(fa_submissions, mapping):
    """Return submissions that were not mapped to an existing WZL submission.

    Args:
        fa_submissions: List of FA submissions
        mapping: List of mappings

    Returns:
        set: Set of unmapped submissions
    """
    mapped = set(m[0] for m in mapping)
    subs = set(fa_submissions)

    return subs - mapped


def create_unmapped_folders(fa_sess, wzl_sess, mapping, exclude=None):
    """Creates folders that aren't found in a mapping, on Weasyl.

    Args:
        fa_sess: The FA session
        wzl_sess: The Weasyl session
        mapping: The mapping list
        exclude: Optional list of FA folders to exclude
    """
    unmapped_folders = get_unmapped_folders(fa_sess.folders, mapping)

    mapping_dict = {fa_folder: wzl_folder for fa_folder, wzl_folder in mapping}

    for folder in fa_sess.folders:
        if folder in unmapped_folders and (
                        exclude is None or folder not in exclude):
            new_wzl_folder = wzl_sess.create_folder(folder.title)

            for subfolder in folder.children:
                if subfolder in unmapped_folders and (
                                exclude is None or subfolder not in exclude):
                    wzl_sess.create_folder(subfolder.title, new_wzl_folder.id)

        else:
            for subfolder in folder.children:
                if subfolder in unmapped_folders and (
                                exclude is None or subfolder not in exclude) \
                        and folder in mapping_dict:
                    wzl_sess.create_folder(subfolder.title,
                                           mapping_dict[folder].id)
