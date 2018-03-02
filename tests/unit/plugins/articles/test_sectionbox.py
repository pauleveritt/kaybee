import pytest
from sphinx.errors import SphinxError

from kaybee.plugins.articles.sectionbox import SectionboxWidget


@pytest.fixture()
def dummy_sectionbox():
    yaml = """
name: vp1
    """
    vp = SectionboxWidget('widget1', 'widget1', yaml)
    yield vp


@pytest.fixture()
def dummy_bad_sectionbox():
    yaml = """
name: vp1
xxx: 99
    """
    vp = SectionboxWidget('widget1', 'widget1', yaml)
    yield vp


class TestSectionbox:
    def test_import(self):
        assert 'SectionboxWidget' == SectionboxWidget.__name__

    def test_construction(self, dummy_sectionbox: SectionboxWidget):
        assert 'vp1' == dummy_sectionbox.props.name

    def test_bad_construction(self):
        yaml = """
        name: vp1
        xxx: 99
            """
        with pytest.raises(SphinxError):
            SectionboxWidget('widget1', 'widget1', yaml)
