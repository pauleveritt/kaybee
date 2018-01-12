from kaybee import app
from kaybee.plugins.resources.directive import ResourceDirective


class TestResourceDirective:
    def test_import(self):
        assert 'ResourceDirective' == ResourceDirective.__name__

    def test_construction(self, dummy_directive):
        assert 'dummy_directive' == dummy_directive.name

    def test_get_resource_class(self, monkeypatch,
                                dummy_directive_class,
                                dummy_resource_class,
                                kb_app):
        # Setup fake registry
        monkeypatch.setattr(app, 'kb', kb_app)
        drc = dummy_directive_class.name
        kb_app.config.resources = {drc: dummy_resource_class}

        actual = ResourceDirective.get_resource_class(drc)
        assert dummy_resource_class == actual

    def test_docname(self, dummy_directive):
        assert 'somedoc' == dummy_directive.docname

    def test_resources(self, dummy_directive):
        assert dict() == dummy_directive.resources

    def test_run_no_reference(self, monkeypatch,
                              dummy_directive_class,
                              dummy_resource_class,
                              dummy_directive, kb_app):
        # Setup fake registry
        monkeypatch.setattr(app, 'kb', kb_app)
        drc = dummy_directive_class.name
        kb_app.config.resources = {drc: dummy_resource_class}

        assert [] == dummy_directive.run()
        assert 'somedoc' in dummy_directive.resources

    def test_run_reference(self, monkeypatch, mocker,
                           dummy_directive_class,
                           dummy_resource_class,
                           dummy_directive,
                           dummy_reference,
                           dummy_references,
                           kb_app):
        # Setup fake registry
        monkeypatch.setattr(app, 'kb', kb_app)
        drc = dummy_directive_class.name
        kb_app.config.resources = {drc: dummy_resource_class}

        # Make this resource class into a reference
        dummy_resource_class.is_reference = True
        kb_app.config.references = dict(
            category=dict(
                category1=dummy_reference
            )
        )
        mocker.patch.object(dummy_references, 'add_reference')
        dummy_directive.run()
        somedoc = dummy_directive.resources['somedoc']
        dummy_references.add_reference.assert_called_once_with(
            'dummy_directive', 'somelabel', somedoc
        )
