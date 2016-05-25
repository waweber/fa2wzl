import logging

logger = logging.getLogger("fa2wzl")
"""Logger instance"""

formatter = logging.Formatter("%(name)s: %(message)s")
handler = logging.StreamHandler()

handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
