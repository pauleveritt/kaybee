import pytest
from sphinx.application import Sphinx

from kaybee.plugins.references.container import ReferencesContainer
from kaybee.plugins.references.handlers import (
    add_document_reference,
    initialize_references_container,
    references_into_html_context,
    register_references,
    validate_references,
    missing_reference,
    dump_settings,
    reference_fieldnames,
    get_reference_classes,
)


class TestInitializeContainer:
    def test_import(self):
        assert 'initialize_references_container' == \
               initialize_references_container.__name__

    def test_construction(self, references_kb_app, sphinx_app, sphinx_env):
        initialize_references_container(
            references_kb_app, sphinx_app, sphinx_env, []
        )
        assert ReferencesContainer == sphinx_app.references.__class__


class TestRegisterReferences:
    def test_import(self):
        assert 'register_references' == register_references.__name__

    def test_is_reference(self, references_kb_app,
                          references_sphinx_app: Sphinx,
                          sphinx_env,
                          valid_registration):
        # It's there by default, which is dumb testing fixturing. For
        # this test, we want to make sure it gets added, so let's remove
        # it first.
        del references_sphinx_app.references['reference']
        register_references(references_kb_app,
                            references_sphinx_app,
                            sphinx_env,
                            []
                            )
        assert 'reference' in references_sphinx_app.references

    def test_not_is_reference(self, references_kb_app,
                              references_sphinx_app: Sphinx,
                              sphinx_env,
                              valid_registration
                              ):
        # It's there by default, which is dumb testing fixturing. For
        # this test, we want to make sure it doesn't get added, so let's
        # remove it first.
        del references_sphinx_app.references['reference']

        # Make Category into a non-reference
        references_kb_app.config.resources['reference'].is_reference = False
        register_references(references_kb_app,
                            references_sphinx_app,
                            sphinx_env,
                            []
                            )
        assert 'reference' not in references_sphinx_app.references


class TestAddDocumentReferences:
    def test_import(self):
        assert 'add_document_reference' == add_document_reference.__name__

    def test_run(self, references_kb_app, sphinx_app, references_sphinx_env,
                 dummy_reference):
        sphinx_app.resources['reference1'] = dummy_reference
        add_document_reference(references_kb_app, sphinx_app,
                               references_sphinx_env)
        reference1 = sphinx_app.references['reference']['reference1']
        assert 'reference1' == reference1.docname


class TestValidateReferences:
    def test_import(self):
        assert 'validate_references' == validate_references.__name__

    def test_missing_reference_type(self, references_kb_app, html_builder,
                                    references_sphinx_env):
        # Resource points at a reference type (e.g. 'reference') that
        # isn't registered
        references_sphinx_env.app.references = dict()
        with pytest.raises(KeyError):
            validate_references(references_kb_app, html_builder,
                                references_sphinx_env)

    def test_missing_reference_value(self, references_kb_app, html_builder,
                                     references_sphinx_env):
        # Resource points at a reference type (e.g. 'reference') that
        # *is* registered, but then at a reference lable that isn't
        references_sphinx_env.app.references['reference'] = dict()

        with pytest.raises(KeyError):
            validate_references(references_kb_app, html_builder,
                                references_sphinx_env)

    def test_runs(self, references_kb_app, html_builder,
                  references_sphinx_env):
        validate_references(references_kb_app, html_builder,
                            references_sphinx_env)


class TestMissingReference:
    def test_import(self):
        assert 'missing_reference' == missing_reference.__name__

    def test_explicit(self, references_kb_app,
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
            reftarget='reference-reference1',
            refexplicit=True
        )
        newnode = missing_reference(references_kb_app, sphinx_app,
                                    references_sphinx_env, node,
                                    dummy_contnode)
        references.get_reference.assert_called_once_with(
            'reference', 'reference1'
        )
        sphinx_app.builder.get_relative_uri.assert_called_once_with(
            node['refdoc'], article1.docname
        )
        assert 'first' == newnode[0][0]

    def test_value_error(self, references_kb_app,
                         sphinx_app,
                         references_sphinx_env,
                         dummy_contnode,
                         ):
        node = dict(
            refdoc=None,
            reftarget='xxx',
        )
        result = missing_reference(references_kb_app, sphinx_app,
                                   references_sphinx_env, node,
                                   dummy_contnode)
        assert None is result

    def test_no_target(self, references_kb_app,
                       sphinx_app,
                       references_sphinx_env,
                       dummy_contnode,
                       ):
        node = dict(
            refdoc=None,
            reftarget='xxx-yyy',
        )
        result = missing_reference(references_kb_app, sphinx_app,
                                   references_sphinx_env, node,
                                   dummy_contnode)
        assert None is result

    def test_not_explicit(self, references_kb_app,
                          sphinx_app,
                          html_builder, references_sphinx_env,
                          dummy_contnode,
                          mocker):
        resources = references_sphinx_env.app.resources
        references = references_sphinx_env.app.references
        article1 = resources['article1']
        article1.title = 'not explicit title'
        mocker.patch.object(references, 'get_reference',
                            return_value=article1)
        mocker.patch.object(sphinx_app.builder, 'get_relative_uri',
                            return_value=9)
        node = dict(
            refdoc=article1,
            reftarget='reference-reference1',
            refexplicit=False
        )
        newnode = missing_reference(references_kb_app, sphinx_app,
                                    references_sphinx_env, node,
                                    dummy_contnode)
        references.get_reference.assert_called_once_with(
            'reference', 'reference1'
        )
        sphinx_app.builder.get_relative_uri.assert_called_once_with(
            node['refdoc'], article1.docname
        )
        assert 'not explicit title' == newnode[0][0]


class TestReferencesIntoHtml:
    def test_import(self):
        assert 'references_into_html_context' == \
               references_into_html_context.__name__

    def test_run(self, references_kb_app, sphinx_app,
                 references_sphinx_env):
        context = dict()
        references_into_html_context(references_kb_app, sphinx_app,
                                     '', '', context, dict())
        assert 'references' in context


class TestReferencesDumpSettings:
    def test_import(self):
        assert 'dump_settings' == dump_settings.__name__

    def test_result(self, references_kb_app, sphinx_env,
                    dummy_reference):
        references_kb_app.config.resources = dict()
        sphinx_env.app.resources = dict()
        sphinx_env.app.references = dict(
            reference=dict(
                reference1=dummy_reference
            )
        )
        result = dump_settings(references_kb_app, sphinx_env)
        assert 'references' in result
        reference = result['references']['values']['reference']
        assert 'reference1' == reference['reference1']['docname']


class TestUtilityFunctions:
    def test_imports(self):
        assert 'reference_fieldnames' == reference_fieldnames.__name__
        assert 'get_reference_classes' == get_reference_classes.__name__

    def test_reference_fieldnames(self, dummy_article):
        results = reference_fieldnames(dummy_article)
        assert 'reference' in results

    def test_get_reference_classes(self, dummy_reference, dummy_article):
        resource_classes = [
            dummy_reference.__class__,
            dummy_article.__class__
        ]
        results = get_reference_classes(resource_classes)
        assert dummy_reference.__class__ == results[0]
