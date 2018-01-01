from kaybee.plugins.resources.container import ResourcesContainer


class TestPluginResourcesContainer:
    def test_import(self):
        assert 'ResourcesContainer' == ResourcesContainer.__name__

    def test_construction(self):
        rc = ResourcesContainer()
        assert 0 == len(rc.keys())

    def test_setitem(self):
        rc = ResourcesContainer()
        rc['foo'] = 9
        assert 'foo' in rc
