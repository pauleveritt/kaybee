import dectate
import pytest

from kaybee.plugins.postrenderer.action import PostrendererAction


class TestPostrenderAction:
    def test_import(self):
        assert 'PostrendererAction' == PostrendererAction.__name__

    def test_construction(self, postrenderer_kb_app):
        dectate.commit(postrenderer_kb_app)
        assert True

    def test_identifier_default(self):
        da = PostrendererAction('resources')
        assert 'resources' == da.identifier([])

    def test_identifiers_conflict(self, postrenderer_kb_app,
                                  conflicting_events):
        # We provide two handlers for same event without distinguishing
        # by order
        with pytest.raises(dectate.error.ConflictError):
            dectate.commit(postrenderer_kb_app)

    def test_get_callbacks(self, postrenderer_kb_app, register_valid_event):
        callbacks = PostrendererAction.get_callbacks(postrenderer_kb_app)
        assert register_valid_event == callbacks[0]
