"""Test level module conftest for technitium_rac package."""

import httpx
import pytest
import requests

# def is_responsive(url) -> bool:
#     """Test response from http server."""
#     try:
#         response = requests.get(url, timeout=(5.0, 3))
#         if response.status_code == 200:
#             return True
#     except ConnectionError:
#         return False


# @pytest.fixture(scope="session")
# def dns_service(docker_ip, docker_services):
#     """Ensure that HTTP service is up and responsive."""
#     # `port_for` takes a container port and returns the corresponding host port
#     port = docker_services.port_for("dns-server", 5380)
#     url = "http://{0}:{1}".format(docker_ip, port)
#     print("url: {0}".format(url))
#     docker_services.wait_until_responsive(
#         timeout=60.0,
#         pause=0.5,
#         check=lambda: is_responsive(url),
#     )
#     return url


@pytest.fixture(scope="session")
def token() -> str:
    response = httpx.get("http://127.0.0.1:5380/api/user/login?user=admin&pass=testing")
    r_dict = response.json()
    if r_dict.get("status", "") == "ok":
        return r_dict.get("token", "")
    return ""
