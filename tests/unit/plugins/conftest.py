import pytest
from kaybee.plugins.resources.base_resource import BaseResource


@pytest.fixture
def sample_resources():
    root = BaseResource('index', 'resource', '')
    root.title = 'Root'
    about = BaseResource('about', 'resource', '')
    about.title = 'About'
    r1 = BaseResource('r1/index', 'resource', '')
    r1.title = 'R1'
    r1about = BaseResource('r1/about', 'resource', '')
    r1about.title = 'R1 About'
    r2 = BaseResource('r1/r2/index', 'resource', '')
    r2.title = 'R2'
    r2about = BaseResource('r1/r2/about', 'resource', '')
    r2about.title = 'R2 About'
    r3 = BaseResource('r1/r2/r3/index', 'resource', '')
    r3.title = 'R3'
    r3about = BaseResource('r1/r2/r3/about', 'resource', '')
    r3about.title = 'R3 About'
    r4 = BaseResource('r1/r2/r3/r4/index', 'resource', '')
    r4.title = 'R4'
    r4about = BaseResource('r1/r2/r3/r4/about', 'resource', '')
    r4about.title = 'R4 About'

    resources = dict()
    for r in (root, about,
              r1, r1about,
              r2, r2about,
              r3, r3about,
              r4, r4about,
              ):
        resources[r.docname] = r

    yield resources
