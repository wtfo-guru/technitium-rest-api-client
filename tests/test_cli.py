"""Module test_cli for package tests from library technitium-rest-api-client."""


def test_token(token: str) -> None:
    """Validate test token.

    :param token: server token
    :type token: str
    """
    print("token: {0}".format(token))
    assert token
