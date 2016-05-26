from fa2wzl.mapping import MappedAttribute


def _folder_loader(folder):
    folder._session._load_folders()


def _folder_content_loader(folder):
    folder.submissions = folder._session._scan_gallery(folder.id)


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
        type (str): The submission type
        title (str): The submission title
        thumbnail_url (str): URL to the thumbnail
    """
    id = None

    # funny that the mapped attribute never gets used
    type = MappedAttribute(None)
    title = MappedAttribute(None)
    thumbnail_url = MappedAttribute(None)

    def __repr__(self):
        return "<Submission #%r: %r>" % (self.id, self.title)
