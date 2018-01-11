from kaybee.plugins.references.base_reference import (
    BaseReference,
    BaseReferenceModel
)


class TestBases:
    def test_imports(self):
        assert 'BaseReference' == BaseReference.__name__
        assert 'BaseReferenceModel' == BaseReferenceModel.__name__
