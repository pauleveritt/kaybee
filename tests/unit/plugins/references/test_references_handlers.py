import dectate
import pytest
from sphinx.application import Sphinx

from kaybee.plugins.references.container import ReferencesContainer
from kaybee.plugins.references.handlers import (
    initialize_references_container,
    register_references,
    validate_references,
    missing_reference,
)


@pytest.fixture()
def valid_registration(kb_app):
    @kb_app.reference('category')
    def category1(*args):
        return

    dectate.commit(kb_app)
    yield category1


class TestInitializeContainer:
    def test_import(self):
        assert 'initialize_references_container' == \
               initialize_references_container.__name__

    def test_construction(self, kb_app, sphinx_app, sphinx_env):
        initialize_references_container(
            kb_app, sphinx_app, sphinx_env, []
        )
        assert ReferencesContainer == sphinx_app.references.__class__


class TestRegisterReferences:
    def test_import(self):
        assert 'register_references' == register_references.__name__

    def test_run(self, kb_app, references_sphinx_app: Sphinx,
                 sphinx_env,
                 valid_registration):
        register_references(kb_app,
                            references_sphinx_app,
                            sphinx_env,
                            []
                            )


class TestValidateReferences:
    def test_import(self):
        assert 'validate_references' == validate_references.__name__


class TestMissingReference:
    def test_import(self):
        assert 'missing_reference' == missing_reference.__name__
