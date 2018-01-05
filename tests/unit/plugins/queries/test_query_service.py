from kaybee.plugins.queries.service import Query


class TestQueryService:
    def test_import(self):
        assert 'Query' == Query.__name__

    def test_filter(self):
        collection = dict(x=1)
        actual = Query.filter(collection)
        assert collection == actual
