from kaybee.plugins.queries.handlers import (
    initialize_query_service,
)


class TestQueriesHandlers:
    def test_import(self):
        assert 'initialize_query_service' == \
               initialize_query_service.__name__

    def test_initialize_query_service(self, kb_app, sphinx_app, sphinx_env):
        initialize_query_service(kb_app, sphinx_app, sphinx_env, [])
        assert {} == sphinx_app.query
