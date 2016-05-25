import datetime
import re
from contextlib import contextmanager

import requests
import time

from lxml import html

from fa2wzl import constants, exceptions
from fa2wzl.fa.models import Folder, Submission
from fa2wzl.logging import logger


class FASession(object):
    """A FurAffinity session.

    """

    def __init__(self, username):
        """Construct a new FA session.

        Args:
            username (str): The username to use
        """
        self.username = username

        self._requests = requests.Session()
        self._requests.headers["User-Agent"] = constants.USER_AGENT
        self._requests.headers["Referer"] = constants.FA_ROOT + "/"

        self._rate_limit_start = datetime.datetime.now()
        self._rate_limit_count = 0

        self._folders = {}
        self._submissions = {}

    def _limited_call(self, func, *args, **kwargs):
        """Rate limit calls to a function.
        """

        # Check seconds that have passed
        now = datetime.datetime.now()
        diff = (now - self._rate_limit_start).total_seconds()

        if diff >= 60:
            # If greater than a minute, reset the rate limit
            self._rate_limit_count = 0
            self._rate_limit_start = now
        else:
            # Check if the per-minute limit has been exceeded
            if self._rate_limit_count >= constants.FA_PAGE_REQUESTS_PER_MINUTE:
                # Wait until next minute, then reset the count/time
                wait_time = 60 - diff
                logger.debug("Hit rate limit, waiting %d seconds" % wait_time)
                time.sleep(wait_time)
                self._rate_limit_count = 0
                self._rate_limit_start = datetime.datetime.now()

        self._rate_limit_count += 1

        return func(*args, **kwargs)

    def _html_get(self, *args, **kwargs):
        res = self._requests.get(*args, **kwargs)
        # Explicitly decode the bytes from UTF-8 instead of letting requests do
        # it, since it appears to decode the string twice for some reason
        doc = html.fromstring(res.content.decode("utf-8"))
        return doc

    def _html_post(self, *args, **kwargs):
        res = self._requests.post(*args, **kwargs)
        doc = html.fromstring(res.content.decode("utf-8"))
        return doc

    def get_captcha(self):
        """Get a CAPTCHA puzzle.

        Returns:
            bytes: A JPEG image.
        """
        res = self._limited_call(self._requests.get,
                                 constants.FA_ROOT + "/captcha.jpg")
        data = res.content
        return data

    @contextmanager
    def login(self, password, captcha):
        """Log in to the site.

        Call .logout to log out, or use this method with the context manager.

        Args:
            password (str): The password
            captcha (str): The CAPTCHA solution

        Raises:
            AuthenticationError: If login fails
        """
        try:
            url = constants.FA_ROOT + "/login/"
            data = {
                "action": "login",
                "name": self.username,
                "pass": password,
                "captcha": captcha,
                "login": "Login to\u00a0FurAffinity",
            }

            logger.info("Logging in as %s" % self.username)
            self._limited_call(self._requests.post, url, data=data)

            if "a" not in self._requests.cookies or \
                            "b" not in self._requests.cookies:
                raise exceptions.AuthenticationError()

            yield
        finally:
            self.logout()

    def logout(self):
        """Log out of the site.
        """
        logger.info("Logging out")
        self._limited_call(self._requests.get, constants.FA_ROOT + "/logout/")

    def _load_folders(self):
        logger.debug("Loading folders")

        url = constants.FA_ROOT + "/controls/folders/submissions/"
        doc = self._limited_call(self._html_get, url)

        # get groups
        for group_el in doc.cssselect(".group-row"):
            try:
                title = str(group_el.cssselect("strong")[0].text_content())

                id_match = re.search("group-([0-9]+)", group_el.get("class"))
                id = int(id_match.group(1))

                group = self._folders.get(id)
                if group is None:
                    group = Folder()
                    group._session = self
                    group.id = id
                    self._folders[id] = group

                group.title = title
                group.children = []
                group.submissions = []
            except (IndexError, ValueError):
                raise exceptions.ScraperError()

        # Get folders
        for folder_el in doc.cssselect(".folder-row"):
            try:
                title = str(folder_el.cssselect(".folder-name strong")[
                                0].text_content())
                id_match = re.search("folder-([0-9]+)", folder_el.get("class"))
                group_match = re.search("group-([0-9]+)", group_el.get("class"))

                id = int(id_match.group(1))
                parent_id = int(group_match.group(1))

                folder = self._folders.get(id)
                if folder is None:
                    folder = Folder()
                    folder._session = self
                    folder.id = id
                    self._folders[id] = folder

                folder.title = title
                folder.children = []

                parent = self._folders.get(parent_id)
                if parent is not None:
                    parent.children.append(folder)

            except (IndexError, ValueError):
                raise exceptions.ScraperError()

    def get_folder(self, id):
        """Get a folder by ID.

        Args:
            id (int): The folder ID

        Returns:
            The folder.

        Raises:
            KeyError: If the folder does not exist.
        """
        if id in self._folders:
            return self._folders[id]

        self._load_folders()
        return self._folders[id]

    def get_folders(self):
        """Get a dict of the user's folders.
        """

        if len(self._folders) == 0:
            self._load_folders()

        return dict(self._folders)

    def _scan_submission_page(self, url_format):
        """Return submissions found in pages of a base url.

        Args:
            url_format (str): URL, with a %d that holds the page id

        Returns:
            A list of submission objects.
        """

        submissions = []

        try:
            page = 1
            while True:
                url = url_format % page
                doc = self._limited_call(self._html_get, url)
                logger.debug("Scanning submissions from %s" % url)

                count = 0

                for el in doc.cssselect(".gallery > *"):
                    if el.get("id") == "no-images":
                        continue

                    id_str = el.get("id")[4:]
                    if id_str == "":
                        continue

                    id = int(id_str)

                    submission = self._submissions.get(id)
                    if submission is None:
                        submission = Submission()
                        submission._session = self
                        submission.id = id
                        self._submissions[id] = submission

                    submission.title = str(
                        el.cssselect("span")[0].text_content())

                    if "r-adult" in el.classes:
                        submission.rating = "adult"
                    elif "r-mature" in el.classes:
                        submission.rating = "mature"
                    elif "r-general" in el.classes:
                        submission.rating = "general"
                    else:
                        raise exceptions.ScraperError()

                    submission.thumbnail_url = "https:" + el.cssselect("img")[
                        0].get("src")

                    submissions.append(submission)
                    count += 1

                if count == 0:
                    break

                logger.debug("Found %d submissions" % count)

                page += 1

        except (IndexError, ValueError):
            raise exceptions.ScraperError()

        return submissions

    def _scan_gallery(self):
        logger.debug("Scanning gallery")
        url = constants.FA_ROOT + "/gallery/%s/%%d/" % self.username
        submissions = self._scan_submission_page(url)
        return submissions

    def _scan_scraps(self):
        logger.debug("Scanning scraps")
        url = constants.FA_ROOT + "/scraps/%s/%%d/" % self.username
        submissions = self._scan_submission_page(url)
        return submissions

    def _scan_folder(self, folder):
        logger.debug("Scanning folder %r" % folder)

        url = constants.FA_ROOT + "/gallery/%s/folder/%d/-/%%d/" % (
            self.username, folder.id)
        submissions = self._scan_submission_page(url)

        folder.submissions = []

        for sub in submissions:
            folder.submissions.append(sub)

    def _load_submission(self, id):
        url = constants.FA_ROOT + "/view/%d/" % id
        doc = self._limited_call(self._html_get, url)

        sub = self._submissions.get(id)
        if sub is None:
            sub = Submission()
            sub._session = self
            sub.id = id
            self._submissions[id] = sub

        try:
            sub.title = doc.cssselect("#submissionImg")[0].get("alt")
            for el in doc.cssselect(".submission.button a"):
                if str(el.text_content()) == "Download":
                    sub.media_url = "https:" + el.get("href")

            rating_classes = doc.cssselect(".rating-box")[0].classes
            if "adult" in rating_classes:
                sub.rating = "adult"
            elif "mature" in rating_classes:
                sub.rating = "mature"
            elif "general" in rating_classes:
                sub.rating = "general"
            else:
                raise exceptions.ScraperError()

            sub.description = str(doc.cssselect(".p20")[0].text_content())
            sub.tags = []

            for el in doc.cssselect(".tags-row .tags a"):
                tag_name = str(el.text_content())
                sub.tags.append(tag_name)

            # date_str = str(
            #     doc.cssselect("#submission_page .popup-date")[0].get("title"))
            #
            # parsed_date = datetime.datetime.strptime(date_str, "%b %-d")

            return sub
        except (IndexError, ValueError):
            raise exceptions.ScraperError()
