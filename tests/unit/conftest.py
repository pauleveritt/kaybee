import pytest


@pytest.fixture()
def app_minimum():
    app = dict()
    yield app
