"""Top level module cli for technitium_rac package."""

from typing import Optional

from technitium_rac.configurator import app_config


def _all_servers() -> str:
    """_all_servers return a comma-delimited list of all configured servers.

    :raises ValueError: If no servers are configured
    :return: comma-delimited list of all configured servers
    :rtype: str
    """
    if app_config.servers:
        return ",".join(app_config.servers.keys())
    raise ValueError(
        "You must specify a servers in your config file to use all.",
    )


def reconcile_servers(servers: Optional[tuple[str, ...]]) -> str:
    """reconcile_servers return a comma-delimited list of server keys.

    :param servers: Tuple of server keys
    :type servers: Optional[tuple[str, ...]]
    :raises ValueError: If server si none and config default_servers is not set
    :raises KeyError: KeyError if one of servers is not in config
    :return: a comma-delimited list of server keys
    :rtype: str
    """
    if servers is None:
        if app_config.default_servers:
            return app_config.default_servers
        raise ValueError(
            "You must specify a server via command line or set the default_servers in your config file.",  # noqa: E501
        )
    if len(servers) == 1 and servers[0].lower() == "all":
        return _all_servers()
    s_list: list[str] = []
    for server in servers:
        if server in app_config.servers:
            s_list.append(server)
        else:
            raise KeyError(
                "Server {0} not found in config file servers dict.".format(server),
            )
    return ",".join(s_list)
