from kaybee.plugins.layouts.base_layout import BaseLayout


class TestBaseLayout:
    def test_import(self):
        assert 'BaseLayout' == BaseLayout.__name__

    def test_construction(self):
        bl = BaseLayout(**dict(flag=99))
        assert 'flag' not in bl.settings
        assert None is bl.sphinx_app