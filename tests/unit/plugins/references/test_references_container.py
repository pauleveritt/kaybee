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

    def test_missing_reftype(self, sample_container: ReferencesContainer):
        with pytest.raises(KeyError):
            sample_container['article']['flask'] = dict(flag=9)

    def test_existing_reftype(self, sample_container: ReferencesContainer):
        sample_container['article'] = dict()
        sample_container['article']['flask'] = dict(flag=9)

    def test_add_reference(self, sample_container: ReferencesContainer):
        sample_container['reference'] = dict()
        sample_container.add_reference('reference', 'reference1', 999)
        result = sample_container['reference']['reference1']
        assert 999 == result

    def test_get_reference(self, sample_container: ReferencesContainer):
        sample_container['reference'] = dict()
        sample_container.add_reference('reference', 'reference1', 999)
        result = sample_container.get_reference('reference', 'reference1')
        assert 999 == result

    def test_get_no_reference(self, sample_container: ReferencesContainer):
        sample_container['reference'] = dict()
        sample_container.add_reference('reference', 'reference1', 999)
        result = sample_container.get_reference('xxx', 'yyy')
        assert None is result

    def test_resource_references(self, references_sphinx_app,
                                 dummy_resource, dummy_reference):
        references = references_sphinx_app.env.references
        results = references.resource_references(dummy_resource)
        assert dummy_reference == results['reference'][0]
