import dectate
import pytest

from kaybee.plugins.genericpage.action import GenericpageAction


class TestGenericpageAction:
    def test_import(self):
        assert 'GenericpageAction' == GenericpageAction.__name__

    def test_construction(self, genericpages_kb_app):
        dectate.commit(genericpages_kb_app)
        assert True

    def test_identifier_default(self):
        da = GenericpageAction()
        assert '40' == da.identifier([])

    def test_identifiers_conflict(self, genericpages_kb_app, conflicting_gps):
        with pytest.raises(dectate.error.ConflictError):
            dectate.commit(genericpages_kb_app)

    def test_get_builtin_genericpage(self, genericpages_kb_app):
        # No @kb.genericpage found in the docs project or any plugins it
        # installed, so get_genericpage should return the built-in class,
        # since none in registry.
        dectate.commit(genericpages_kb_app)
        gp = GenericpageAction.get_genericpage(genericpages_kb_app)
        assert 'Genericpage' == gp.__name__

    def test_get_single_genericpage(self, genericpages_kb_app, valid_gp):
        # The docs project (or a third-party plugin) registers a single
        # "override"
        gp = GenericpageAction.get_genericpage(genericpages_kb_app)
        assert valid_gp == gp

    def test_get_sorted_genericpage(self, genericpages_kb_app, valid_gps):
        gp = GenericpageAction.get_genericpage(genericpages_kb_app)
        assert valid_gps[1] == gp
