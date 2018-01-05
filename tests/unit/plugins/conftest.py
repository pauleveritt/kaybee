import pytest
from kaybee.plugins.resources.base_resource import BaseResource


@pytest.fixture
def sample_resources():
    root = BaseResource('index', 'resource', '')
    about = BaseResource('about', 'resource', '')
    r1 = BaseResource('r1/index', 'resource', '')
    r1about = BaseResource('r1/about', 'resource', '')
    r2 = BaseResource('r1/r2/index', 'resource', '')
    r2about = BaseResource('r1/r2/about', 'resource', '')
    r3 = BaseResource('r1/r2/r3/index', 'resource', '')
    r3about = BaseResource('r1/r2/r3/about', 'resource', '')
    r4 = BaseResource('r1/r2/r3/r4/index', 'resource', '')
    r4about = BaseResource('r1/r2/r3/r4/about', 'resource', '')

    resources = dict()
    for r in (root, about,
              r1, r1about,
              r2, r2about,
              r3, r3about,
              r4, r4about,
              ):
        resources[r.docname] = r

    yield resources
