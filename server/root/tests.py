from server.root.db import build_url


def test_build_db_url_full():
    """Test: build full db connection string like: engine://user:password@host:port/name"""

    assert build_url({
        "engine": "engine",
        "name": "name",
        "user": "user",
        "password": "password",
        "host": "host",
        "port": 0,
    }) == "engine://user:password@host:0/name"


def test_build_db_url_no_password():
    """Test: build db connection string like: engine://user@host:0/name"""

    assert build_url({
        "engine": "engine",
        "name": "name",
        "user": "user",
        "host": "host",
        "port": 0,
    }) == "engine://user@host:0/name"


def test_build_db_url_no_port():
    """Test: build db connection string like: engine://user:password@host/name"""

    assert build_url({
        "engine": "engine",
        "name": "name",
        "user": "user",
        "password": "password",
        "host": "host",
    }) == "engine://user:password@host/name"


def test_build_db_url_no_credentials():
    """Test: build db connection string like: engine://host:0/name"""

    assert build_url({
        "engine": "engine",
        "name": "name",
        "host": "host",
        "port": 0,
    }) == "engine://host:0/name"


def test_build_db_url_no_credentials_and_location():
    """Test: build db connection string like: engine://name"""

    assert build_url({
        "engine": "engine",
        "name": "name",
    }) == "engine://name"
