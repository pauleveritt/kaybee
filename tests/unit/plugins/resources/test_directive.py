from kaybee.plugins.resources.directive import ResourceDirective
from kaybee import app


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

    def test_docname(self, mocker, dummy_directive):
        assert 'somedoc' == dummy_directive.docname

    def test_resources(self, mocker, dummy_directive):
        assert dict() == dummy_directive.resources

    def test_run_result(self, monkeypatch,
                        dummy_directive_class,
                        dummy_resource_class,
                        dummy_directive, kb_app):
        # Setup fake registry
        monkeypatch.setattr(app, 'kb', kb_app)
        drc = dummy_directive_class.name
        kb_app.config.resources = {drc: dummy_resource_class}

        assert [] == dummy_directive.run()
        assert 'somedoc' in dummy_directive.resources
