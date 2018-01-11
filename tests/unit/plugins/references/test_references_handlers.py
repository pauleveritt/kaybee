from kaybee.plugins.references.handlers import (
    initialize_resources_container,
    register_references,
    validate_references,
    missing_reference,
)


class TestInitializeContainer:
    def test_import(self):
        assert 'initialize_resources_container' == \
               initialize_resources_container.__name__


class TestRegisterReferences:
    def test_import(self):
        assert 'register_references' == register_references.__name__


class TestValidateReferences:
    def test_import(self):
        assert 'validate_references' == validate_references.__name__


class TestMissingReference:
    def test_import(self):
        assert 'missing_reference' == missing_reference.__name__
