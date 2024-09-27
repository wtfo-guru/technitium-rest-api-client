"""Top level module cli for technitium_rac package."""

from api_client.endpoint import Endpoint, HTTPMethod
from api_client.request import RestRequest

from technitium_rac.configurator import app_config
from technitium_rac.constants import USER_AGENT


def login(server: str, username: str, password: str) -> str:
    """Login with username and password to get 30 minute token.

    :param server: Server
    :type server: str
    :param username: Username
    :type username: str
    :param password: Password
    :type password: str
    :return: An api token valid for 30 minutes
    :rtype: str
    """
    if server in app_config.servers:
        server_def = app_config.servers.get(server, {})
        if "root" in server_def:
            root: str = server_def.get("root", "")
            endpoint = Endpoint(
                name="login",
                path="/api/settings/{action}",
                request_method=HTTPMethod.GET,
                query_parameters=["username", "password"],
            )
            req = RestRequest(  # noqa: F841
                endpoints=endpoint,
                api_root=root,
                user_agent=USER_AGENT,
            )
    return ""
