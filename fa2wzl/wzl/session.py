import requests
from lxml import html

from fa2wzl import constants, exceptions
from fa2wzl.logging import logger
from fa2wzl.wzl.models import Folder, Submission


class WZLSession(object):
    """A Weasyl session.

    Attributes:
        username (str): The username logged in as
    """

    def __init__(self, api_key):
        self._requests = requests.Session()
        self._requests.headers["X-Weasyl-API-Key"] = api_key

        self._folders = {}
        self._submissions = {}

        self._username = None

        self._root_folders = None
        self._gallery_submissions = None

    @property
    def username(self):
        if self._username is None:
            res = self._requests.get(constants.WZL_ROOT + "/api/whoami")
            self._username = res.json()["login"]

        return self._username

    def _load_folders(self):
        logger.debug("Loading folders")

        self._root_folders = []

        url = constants.WZL_ROOT + "/api/users/%s/view" % self.username
        res = self._requests.get(url)
        folders = res.json()["folders"]

        for folder_struct in folders:
            folder = self._folders.get(folder_struct["folder_id"])
            if folder is None:
                folder = Folder()
                folder._session = self
                folder.id = folder_struct["folder_id"]
                self._folders[folder.id] = folder

            folder.title = folder_struct["title"]
            folder.children = []

            self._root_folders.append(folder)

            if "subfolders" in folder_struct:
                for subfolder_struct in folder_struct["subfolders"]:
                    subfolder = self._folders.get(subfolder_struct["folder_id"])
                    if subfolder is None:
                        subfolder = Folder()
                        subfolder._session = self
                        subfolder.id = subfolder_struct["folder_id"]
                        self._folders[subfolder.id] = subfolder

                    subfolder.title = subfolder_struct["title"]
                    subfolder.children = []

                    folder.children.append(subfolder)

    def _load_submission_from_struct(self, sub_struct):
        id = sub_struct["submitid"]

        sub = self._submissions.get(id)
        if sub is None:
            sub = Submission()
            sub._session = self
            sub.id = id
            self._submissions[id] = sub

        sub.title = sub_struct["title"]
        sub.type = sub_struct["subtype"]
        sub.thumbnail_url = sub_struct["media"]["thumbnail"][0]["url"]

        return sub

    def _scan_gallery(self, folder_id=None):

        next_id = None
        url = constants.WZL_ROOT + "/api/users/%s/gallery" % self.username

        submissions = []

        logger.debug("Scanning gallery folder %r" % folder_id)

        while True:
            params = {}

            if next_id is not None:
                params["nextid"] = next_id

            if folder_id is not None:
                params["folderid"] = folder_id

            res = self._requests.get(url, params=params)
            data = res.json()

            next_id = data["nextid"]

            for sub_struct in data["submissions"]:
                sub = self._load_submission_from_struct(sub_struct)

                submissions.append(sub)

            if next_id is None:
                break

            logger.debug("Found %d submissions" % len(data["submissions"]))

        if folder_id is None:
            self._gallery_submissions = submissions

        return submissions

    def reload_folders(self):
        """Reload the root folders.

        Use after creating new folders.
        """
        self._root_folders = None
        self._load_folders()

    @property
    def folders(self):
        if self._root_folders is None:
            self._load_folders()

        return list(self._root_folders)

    @property
    def gallery(self):
        if self._gallery_submissions is None:
            self._scan_gallery()

        return list(self._gallery_submissions)

    def create_folder(self, title, parent_id=None):
        url = constants.WZL_ROOT + "/control/createfolder"

        data = {
            "title": title,
            "parentid": parent_id,
        }

        logger.info("Creating folder \"%s\" (Parent %r)" % (title, parent_id))

        self._requests.post(url, data=data)

        old_ids = set(self._folders.keys())
        self.reload_folders()
        new_ids = set(self._folders.keys())

        new_id = list(new_ids - old_ids)[0]
        return self._folders[new_id]

    def create_submission(self, file_name, file_obj, title, type, category,
                          rating,
                          description, tags, folder_id=0, thumb_obj=None):
        """Create a submission.

        Args:
            file_name (str): The file name
            file_obj: A file-like object containing the media to upload
            title (str): The submission title
            type (str): The submission type
            category (int): A category code
            rating (int): A rating code
            description (str): A text description
            tags: A list of tag names
            folder_id (int, optional): The parent folder ID
            thumb_obj: An optional thumbnail file-like object 
        """

        if type == "visual":
            url = constants.WZL_ROOT + "/submit/visual"
            files = {
                "submitfile": (file_name, file_obj),
                "thumbfile": "",
            }

            data = {
                "title": title,
                "subtype": category,
                "folderid": folder_id,
                "rating": rating,
                "content": description,
                "tags": " ".join(tags),
            }

        elif type == "literary":
            url = constants.WZL_ROOT + "/submit/literary"
            files = {
                "submitfile": (file_name, file_obj),
                "coverfile": "",
            }

            if thumb_obj is not None:
                files["thumbfile"] = thumb_obj,

            data = {
                "embedlink": "",
                "title": title,
                "subtype": category,
                "folderid": folder_id,
                "rating": rating,
                "content": description,
                "tags": " ".join(tags),
            }

        elif type == "multimedia":
            url = constants.WZL_ROOT + "/submit/multimedia"
            files = {
                "submitfile": (file_name, file_obj),
                "coverfile": "",
            }

            if thumb_obj is not None:
                files["thumbfile"] = thumb_obj,

            data = {
                "embedlink": "",
                "title": title,
                "subtype": category,
                "folderid": folder_id,
                "rating": rating,
                "content": description,
                "tags": " ".join(tags),
            }

        logger.info("Uploading file %s as \"%s\"" % (file_name, title))

        self._requests.post(url, files=files, data=data)
