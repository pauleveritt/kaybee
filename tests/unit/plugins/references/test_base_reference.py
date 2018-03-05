from kaybee.plugins.references.base_reference import (
    BaseReference,
    BaseReferenceModel
)


class TestBases:
    def test_imports(self):
        assert 'BaseReference' == BaseReference.__name__
        assert 'BaseReferenceModel' == BaseReferenceModel.__name__

    def test_get_sources(self, references_sphinx_app):
        resources = references_sphinx_app.env.resources
        references = references_sphinx_app.env.references
        reference1 = references['reference']['reference1']
        result = reference1.get_sources(resources)
        assert 'resource1' == result[0].docname