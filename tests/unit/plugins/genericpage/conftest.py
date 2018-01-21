import dectate
import pytest

from kaybee.plugins.genericpage.genericpage import Genericpage
from kaybee.plugins.genericpage.action import GenericpageAction


@pytest.fixture()
def genericpage_kb_app(kb_app):
    class genericpage_kb_app(kb_app):
        genericpage = dectate.directive(GenericpageAction)

    yield genericpage_kb_app


@pytest.fixture()
def conflicting_gps(genericpage_kb_app):
    @genericpage_kb_app.genericpage()
    class Genericpage1(Genericpage):
        pass

    @genericpage_kb_app.genericpage()
    class Genericpage2(Genericpage):
        pass

    yield (Genericpage1, Genericpage2)


@pytest.fixture()
def valid_gp(genericpage_kb_app):
    @genericpage_kb_app.genericpage()
    class Genericpage1(Genericpage):
        pass

    dectate.commit(genericpage_kb_app)
    yield Genericpage1


@pytest.fixture()
def valid_gps(genericpage_kb_app):
    @genericpage_kb_app.genericpage()
    class Genericpage1(Genericpage):
        pass

    # This one should "override" the first one
    @genericpage_kb_app.genericpage(order=10)
    class Genericpage2(Genericpage):
        pass

    dectate.commit(genericpage_kb_app)
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
