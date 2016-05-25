import requests

from fa2wzl import constants
from fa2wzl.wzl.models import Folder


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

    @property
    def username(self):
        if self._username is None:
            res = self._requests.get(constants.WZL_ROOT + "/api/whoami")
            self._username = res.json()["login"]

        return self._username

    def _load_folders(self):
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
