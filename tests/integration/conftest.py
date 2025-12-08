import pytest

from unittest import mock
from fastapi.testclient import TestClient
from main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session", autouse=True)
def patch_cache():
    """Patch cache decorator for the entire test session."""
    with mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f):
        yield
