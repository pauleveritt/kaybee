from kaybee.plugins.references.container import ReferencesContainer


class TestReferencesContainer:
    def test_import(self):
        assert 'ReferencesContainer' == ReferencesContainer.__name__
