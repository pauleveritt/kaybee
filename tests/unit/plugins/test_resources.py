from kaybee.plugins.resources import (
    handlers
)


class TestResourceHandlers:
    def test_import(self):
        assert 'handle_builderinited' == handlers.handle_builderinited.__name__
