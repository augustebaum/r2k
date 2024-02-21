import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, fields

# from .cli import logger
from .constants import Parser


class LocalFeed(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    url: str
    updated: Optional[datetime.datetime] = None


class Config(BaseModel):
    """Global configuration for the project"""

    feeds: dict[str, LocalFeed] = Field(default_factory=dict)
    # TODO: Instead read from a file
    # Or use SecretStr: https://docs.pydantic.dev/latest/examples/secrets/
    password: str = ""
    kindle_address: str = ""
    send_from: str = ""
    send_to: str = Field(init=False, default="")
    parser: Parser = Parser.READABILITY

    # Internal properties not accessible outside the class
    _path: Optional[str] = fields.PrivateAttr(default=None)
    _loaded: bool = fields.PrivateAttr(default=False)

    def __post_load__(self) -> None:
        """Tasks to perform after loading the config from the YAML"""

        self._loaded = True
        if self.parser == Parser.PUSH_TO_KINDLE:
            kindle_address = self.kindle_address.split("@")[0]
            self.send_to = f"{kindle_address}@pushtokindle.com"
        else:
            self.send_to = self.kindle_address

    def load(self, path: str) -> None:
        """Load configurations from a YAML file"""
        self._path = path

        # logger.debug(f"Loading config from {self._path}")
        with open(self._path) as f:
            file_content = f.read()
            file_config = Config.model_validate_json(file_content)

        self.__dict__.update(file_config)
        self.__post_load__()

    def save(self, path: Optional[str] = None) -> None:
        """Dump the contents of the internal dict to file"""
        if self._path is None:
            if path:
                self._path = path
            else:
                raise FileNotFoundError("Path not set in Config. Need to run config.load before running config.save")

        with open(self._path, "w") as f:
            json_dump = self.model_dump_json(indent=2)
            f.write(json_dump)

    @classmethod
    def fields(cls) -> List[str]:
        """Return a list with all the publicly exposed fields of the Config class"""
        # Ignoring mypy typing validation here, as for some reason it assumes that f.type is always Field, but it isn't
        return list(cls.__fields__.keys())


config = Config()
