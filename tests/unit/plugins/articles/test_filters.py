import pytest

from kaybee.plugins.articles.filters import (
    BaseFilter,
    DatetimeFilter,
)


@pytest.fixture()
def datetime_sphinx_app(sphinx_app):
    yield sphinx_app


@pytest.fixture()
def datetime_filter(datetime_sphinx_app):
    bf = DatetimeFilter(datetime_sphinx_app)
    yield bf


class TestBaseFilter:
    def test_import(self):
        assert 'BaseFilter' == BaseFilter.__name__

    def test_construction(self, sphinx_app):
        bf = BaseFilter(sphinx_app)
        assert sphinx_app == bf.sphinx_app


class TestDatetimeFilter:
    def test_import(self):
        assert 'DatetimeFilter' == DatetimeFilter.__name__

    def test_construction(self, datetime_sphinx_app, datetime_filter):
        assert datetime_sphinx_app == datetime_filter.sphinx_app

    def test_formatting_default(self, datetime_filter, past_datetime):
        result = datetime_filter(past_datetime)
        assert '2012/04/25' == result

    def test_formatting_short(self, datetime_filter, past_datetime):
        result = datetime_filter(past_datetime, 'short')
        assert 'Apr 25' == result
