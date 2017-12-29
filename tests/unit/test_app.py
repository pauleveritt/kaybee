from kaybee.app import kb


class TestApp:
    def test_import(self):
        assert 'kb' == kb.__name__
