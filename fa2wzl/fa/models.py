from fa2wzl.mapping import MappedAttribute


class Folder(object):
    """Represents a submission folder.

    Attributes:
        id (int): The ID on the site
        title (str): The folder title
        children: List of child folders
        submissions: List of submissions in this folder
    """

    id = None
    title = MappedAttribute(None)
    children = MappedAttribute(None)
    submissions = MappedAttribute(None)


class Submission(object):
    """Represents a submission.

    Attributes:
        id (int): The submission ID
        title (str): The submission title
        rating (str): The content rating
        description (str): The description
        tags: A list of tag names
        thumbnail_url (str): URL to the thumbnail
        media_url (str): URL to the media
    """
    id = None
    title = MappedAttribute(None)
    rating = MappedAttribute(None)
    description = MappedAttribute(None)

    tags = MappedAttribute(None)

    thumbnail_url = MappedAttribute(None)
    media_url = MappedAttribute(None)
