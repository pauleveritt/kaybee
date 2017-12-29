import kaybee
from kaybee import setup


class TestSetup:
    def test_import(self):
        assert 'setup' == setup.__name__

    def test_return_value(self):
        result = setup(dict())
        assert kaybee.__version__ == result['version']
        assert False is result['parallel_read_safe']
