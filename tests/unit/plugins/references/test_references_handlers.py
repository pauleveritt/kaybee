import pytest
from sphinx.application import Sphinx

from kaybee.plugins.references.container import ReferencesContainer
from kaybee.plugins.references.handlers import (
    initialize_references_container,
    register_references,
    validate_references,
    missing_reference,
)


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
        assert 'category' in references_sphinx_app.references


class TestValidateReferences:
    def test_import(self):
        assert 'validate_references' == validate_references.__name__

    def test_missing_reference_type(self, kb_app, html_builder,
                                    references_sphinx_env):
        # Resource points at a reference type (e.g. 'category') that
        # isn't registered
        references_sphinx_env.app.references = dict()
        with pytest.raises(KeyError):
            validate_references(kb_app, html_builder, references_sphinx_env)

    def test_missing_reference_value(self, kb_app, html_builder,
                                     references_sphinx_env):
        # Resource points at a reference type (e.g. 'category') that
        # *is* registered, but then at a category lable that isn't
        references_sphinx_env.app.references['category'] = dict()

        with pytest.raises(KeyError):
            validate_references(kb_app, html_builder, references_sphinx_env)

    def test_runs(self, kb_app, html_builder, references_sphinx_env):
        validate_references(kb_app, html_builder, references_sphinx_env)


class TestMissingReference:
    def test_import(self):
        assert 'missing_reference' == missing_reference.__name__

    def test_explicit(self, kb_app,
                      sphinx_app,
                      html_builder, references_sphinx_env,
                      dummy_contnode,
                      mocker):
        resources = references_sphinx_env.app.resources
        references = references_sphinx_env.app.references
        article1 = resources['article1']
        mocker.patch.object(references, 'get_reference',
                            return_value=article1)
        mocker.patch.object(sphinx_app.builder, 'get_relative_uri',
                            return_value=9)
        node = dict(
            refdoc=article1,
            reftarget='category-category1',
            refexplicit=True
        )
        newnode = missing_reference(kb_app, sphinx_app,
                                    references_sphinx_env, node,
                                    dummy_contnode)
        references.get_reference.assert_called_once_with(
            'category', 'category1'
        )
        sphinx_app.builder.get_relative_uri.assert_called_once_with(
            node['refdoc'], article1.docname
        )
        assert 'first' == newnode[0][0]
