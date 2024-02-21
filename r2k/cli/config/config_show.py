import click
import orjson as json
import yaml

from r2k.cli import cli_utils, logger
from r2k.config import config as _config


@click.command("show")
@cli_utils.config_path_option()
def config_show() -> None:
    """Show all the available configuration."""
    logger.info(json.dumps(dict(_config)))
