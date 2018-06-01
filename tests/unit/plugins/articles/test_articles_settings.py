from datetime import datetime

import pytest

from kaybee.plugins.articles.settings import ArticlesModel


@pytest.fixture()
def past_datetime() -> datetime:
    past = datetime(2012, 4, 25, 13, 26)
    yield past


class TestArticlesSettings:
    def test_import(self):
        assert 'ArticlesModel' == ArticlesModel.__name__

    def test_construction(self):
        am = ArticlesModel(**dict(use_toctree=False))
        assert False is am.use_toctree
        assert True is am.json_catalog

    def test_datefmt_short_default(self, past_datetime: datetime):
        am = ArticlesModel(**dict())
        fmt = am.datefmt_short
        result = past_datetime.strftime(fmt)
        assert 'Apr 25' == result

    def test_datefmt_short_custom(self, past_datetime: datetime):
        am = ArticlesModel(**dict(datefmt_short='%b/%d'))
        fmt = am.datefmt_short
        result = past_datetime.strftime(fmt)
        assert 'Apr/25' == result

    def test_datefmt_long_default(self, past_datetime: datetime):
        am = ArticlesModel(**dict())
        fmt = am.datefmt_long
        result = past_datetime.strftime(fmt)
        assert '2012/04/25' == result

    def test_datefmt_full_default(self, past_datetime: datetime):
        am = ArticlesModel(**dict())
        fmt = am.datefmt_full
        result = past_datetime.strftime(fmt)
        assert '2012/04/25 13:26' == result
