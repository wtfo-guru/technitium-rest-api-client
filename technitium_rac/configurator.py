"""Top-level module configurator for technitium_rac package."""

import os
import sys
from pathlib import Path
from typing import Tuple

import click
from yaml_settings_pydantic import (
    BaseYamlSettings,
    YamlFileConfigDict,
    YamlSettingsConfigDict,
)

_TEST = "test"
_PROJECT = "technitium_rac"
_TECHNITIUM_RAC_ENV = os.getenv("TECHNITIUM_RAC_ENV", "prod")
if _TECHNITIUM_RAC_ENV == _TEST and os.getenv("GL_PIPELINE_FLAG", "NO") == "YES":
    _SETTINGS_FILE = Path("./.ci-config.yaml")
else:
    _SETTINGS_FILE = Path().home() / ".config" / "{0}.yaml".format(_PROJECT)


class Common(BaseYamlSettings):  # type: ignore [misc]
    """Common configuration parameters."""

    options: dict[str, int | str | bool]
    servers: dict[str, dict[str, str]]
    default_servers: str = ""  # comma-delimited list
    testing: bool = False
    environ: str = "dunno"

    @property
    def debug(self) -> bool:
        """Debug property."""
        return bool(self.options.get("debug", False))

    @property
    def test(self) -> bool:
        """Test property."""
        return bool(self.options.get(_TEST, False))

    @property
    def verbose(self) -> bool:
        """Verbose property."""
        return bool(self.options.get("verbose", False))

    def initialize(self, **kwargs: bool) -> None:
        """Initialize options."""
        for kk, vv in kwargs.items():
            self.options[kk] = vv

    def server_keys(self) -> set[str]:
        """Return a set of server keys.

        :return: set of server keys
        :rtype: set[str]
        """
        rtn: set[str] = set()
        for server in str(self.options.get("servers", "")).split(","):
            rtn.add(server)
        return rtn

    def server_info(self, name: str) -> Tuple[str, str]:
        """Return the server information.

        :param name: Server identifier one of pri or sec
        :type name: str
        :raises KeyError: If a root url not in config for server
        :raises KeyError: If a token is not in config for server
        :raises KeyError: If server not in config
        :return: The Api root and token for the server
        :rtype: Tuple[str, str]
        """
        s_info: dict[str, str] = self.servers.get(name, {})
        if s_info:
            if "token" in s_info:
                if "root" in s_info:
                    return (s_info["root"], s_info["token"])  # noqa: WPS529
                raise KeyError(
                    "You must provide a root url for server {0}".format(name),
                )
            raise KeyError(
                "You must provide an api token for the server {0} in the config file or login to server {0}".format(  # noqa: E501
                    name,
                ),
            )
        raise KeyError("Server {0} not found in config.".format(name))


class Dev(Common):  # type: ignore [misc]
    """Configuration parameters for dev environment."""

    model_config = YamlSettingsConfigDict(
        yaml_files={_SETTINGS_FILE: YamlFileConfigDict(subpath="dev", required=True)},
    )


class Test(Common):  # type: ignore [misc]
    """Configuration parameters for test environment."""

    testing: bool = True

    model_config = YamlSettingsConfigDict(
        yaml_files={_SETTINGS_FILE: YamlFileConfigDict(subpath=_TEST, required=True)},
    )


class Prod(Common):  # type: ignore [misc]
    """Configuration parameters for prod environment."""

    model_config = YamlSettingsConfigDict(
        yaml_files={_SETTINGS_FILE: YamlFileConfigDict(subpath="prod", required=True)},
    )


_setup = {"dev": Dev, _TEST: Test, "prod": Prod}

# Validate and instantiate specified environment configuration.
try:
    app_config: Dev | Test | Prod
    app_config = _setup[_TECHNITIUM_RAC_ENV]()  # type: ignore[assignment, call-arg]
except ValueError as ex:
    click.echo(str(ex))
    sys.exit(1)
