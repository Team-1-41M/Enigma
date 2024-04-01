import pytest
from passlib.context import CryptContext
from server.root.auth import verify_password
from server.root.crypt import get_crypt_context
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
    }) == "engine:///name"


@pytest.mark.asyncio
async def test_get_crypt_context():
    """Test: get crypt context."""

    context = await get_crypt_context()

    assert context
    assert isinstance(context, CryptContext)


@pytest.mark.asyncio
async def test_verify_password_and_hash_equal():
    """Test: compare the hash of one password with the hash of same password."""

    context = await get_crypt_context()

    plain_password = "password"
    hashed_password = context.hash(plain_password)

    verified: bool = await verify_password(plain_password, hashed_password, context)

    assert verified


@pytest.mark.asyncio
async def test_verify_password_and_hash_not_equal():
    """Test: compare the hash of one password with the hash of another password."""

    context = await get_crypt_context()

    plain_password = "password"
    wrong_password = "wrongpassword"
    hashed_password = context.hash(wrong_password)

    verified: bool = await verify_password(plain_password, hashed_password, context)

    assert not verified
