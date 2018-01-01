import kaybee
from kaybee import setup


class TestInit:
    def test_import(self):
        from kaybee import __version__
        assert isinstance(__version__, str)

    def test_setup_import(self):
        assert 'setup' == setup.__name__

    def test_setup_run(self, mocker, sphinx_app):
        mocker.patch('importscan.scan')
        mocker.patch('dectate.commit')
        mocker.patch.object(sphinx_app, 'add_config_value')
        mocker.patch.object(sphinx_app, 'connect')
        actual = setup(sphinx_app)
        assert kaybee.__version__ == actual['version']
        assert False is actual['parallel_read_safe']
        assert 1 == sphinx_app.add_config_value.call_count
        assert 8 == sphinx_app.connect.call_count
