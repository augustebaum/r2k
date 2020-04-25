from enum import Enum
from os.path import dirname, expanduser, join

CONFIG_ENV_VAR = "RSS_TO_KINDLE_CONFIG"

DEFAULT_APP_PATH = expanduser("~/.r2k")
DEFAULT_CONFIG_PATH = join(DEFAULT_APP_PATH, "config.yml")

PACKAGE_DIR = dirname(__file__)
TOP_LEVEL_DIR = dirname(PACKAGE_DIR)
TEMPLATES_DIR = join(TOP_LEVEL_DIR, "templates")


class Parser(Enum):
    """A convenience class to represent the available parsing options"""

    PUSH_TO_KINDLE = "pushtokindle"
    MERCURY = "mercury"

    __values__ = PUSH_TO_KINDLE, MERCURY
