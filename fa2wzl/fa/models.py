from fa2wzl.mapping import MappedAttribute


def _folder_loader(folder):
    folder._session._load_folders()


def _folder_content_loader(folder):
    folder._session._scan_folder(folder)


def _submission_loader(submission):
    submission._session._load_submission(submission.id)


class Folder(object):
    """Represents a submission folder.

    Attributes:
        id (int): The ID on the site
        title (str): The folder title
        children: List of child folders
        submissions: List of submissions in this folder
    """

    id = None
    title = MappedAttribute(_folder_loader)
    children = MappedAttribute(_folder_loader)
    submissions = MappedAttribute(_folder_content_loader)

    def __repr__(self):
        return "<Folder #%r: %r>" % (self.id, self.title)


class Submission(object):
    """Represents a submission.

    Attributes:
        id (int): The submission ID
        title (str): The submission title
        rating (str): The content rating
        category (str): The submission category
        description (str): The description
        tags: A list of tag names
        thumbnail_url (str): URL to the thumbnail
        media_url (str): URL to the media
    """
    id = None
    title = MappedAttribute(_submission_loader)
    rating = MappedAttribute(_submission_loader)
    category = MappedAttribute(_submission_loader)
    description = MappedAttribute(_submission_loader)

    tags = MappedAttribute(_submission_loader)

    thumbnail_url = MappedAttribute(None)
    media_url = MappedAttribute(_submission_loader)

    def __repr__(self):
        return "<Submission #%r: %r>" % (self.id, self.title)
