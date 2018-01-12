import pytest
from kaybee.plugins.references.container import ReferencesContainer


@pytest.fixture()
def sample_container():
    rc = ReferencesContainer()
    yield rc


class TestReferencesContainer:
    def test_import(self):
        assert 'ReferencesContainer' == ReferencesContainer.__name__

    def test_construction(self, sample_container):
        assert 0 == len(sample_container)

    def test_missing_reftype(self, sample_container):
        with pytest.raises(KeyError):
            sample_container['article']['flask'] = dict(flag=9)

    def test_existing_reftype(self, sample_container):
        sample_container['article'] = dict()
        sample_container['article']['flask'] = dict(flag=9)
