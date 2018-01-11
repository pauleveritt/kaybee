from kaybee.plugins.references.model_types import ReferencesType


class TestReferencesType:
    def test_import(self):
        assert 'ReferencesType' == ReferencesType.__name__
