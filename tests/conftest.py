"""Test level module conftest for technitium_rac package."""

import pytest
import requests


def is_responsive(url):
    """Test response from http server."""
    try:
        response = requests.get(url, timeout=(5.0, 3))
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope="session")
def dns_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""
    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("dns-service", 5380)
    url = "http://{0}:{1}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=30.0,
        pause=0.1,
        check=lambda: is_responsive(url),
    )
    return url
