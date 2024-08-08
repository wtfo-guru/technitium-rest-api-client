"""Module test_cli for package tests from library technitium-rest-api-client."""


def test_token(token) -> None:
    print("token: {0}".format(token))
    assert token
