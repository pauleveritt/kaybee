import kaybee
from kaybee import setup


class TestSetup:
    def test_import(self):
        assert 'setup' == setup.__name__

    def test_return_value(self, sphinx_app):
        result = setup(sphinx_app)
        assert kaybee.__version__ == result['version']
        assert False is result['parallel_read_safe']
