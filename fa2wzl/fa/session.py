import datetime
from contextlib import contextmanager

import requests
import time

from lxml import html

from fa2wzl import constants, exceptions
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
