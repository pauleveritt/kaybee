import dectate
import pytest

from kaybee.plugins.genericpage.genericpage import Genericpage
from kaybee.plugins.genericpage.action import GenericpageAction


@pytest.fixture()
def genericpages_kb_app(kb_app):
    class genericpages_kb_app(kb_app):
        genericpage = dectate.directive(GenericpageAction)

    yield genericpages_kb_app


@pytest.fixture()
def conflicting_gps(genericpages_kb_app):
    @genericpages_kb_app.genericpage()
    class Genericpage1(Genericpage):
        pass

    @genericpages_kb_app.genericpage()
    class Genericpage2(Genericpage):
        pass

    yield (Genericpage1, Genericpage2)


@pytest.fixture()
def valid_gp(genericpages_kb_app):
    @genericpages_kb_app.genericpage()
    class Genericpage1(Genericpage):
        pass

    dectate.commit(genericpages_kb_app)
    yield Genericpage1


@pytest.fixture()
def valid_gps(genericpages_kb_app):
    @genericpages_kb_app.genericpage()
    class Genericpage1(Genericpage):
        pass

    # This one should "override" the first one
    @genericpages_kb_app.genericpage(order=10)
    class Genericpage2(Genericpage):
        pass

    dectate.commit(genericpages_kb_app)
    yield (Genericpage1, Genericpage2)


@pytest.fixture()
def root_resource():
    class Props:
        pass

    class RootResource:
        def __init__(self):
            self.props = Props()

    yield RootResource()


@pytest.fixture()
def foo_doctree():
    class Doctree:
        attributes = dict(source='foo.rst')

    yield Doctree()

@pytest.fixture()
def genericpages_sphinx_app(sphinx_app):
    sphinx_app.env.genericpages = dict()

    yield sphinx_app