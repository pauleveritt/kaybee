import pytest
from sphinx.errors import SphinxError

from kaybee.plugins.articles.base_article import BaseArticleModel
from kaybee.utils.models import load_model
from kaybee.plugins.widgets.base_widget import BaseWidgetModel


class TestLoadModel:
    def test_import(self):
        assert 'load_model' == load_model.__name__

    def test_article_success(self):
        dn = 'index'
        yaml = 'weight: 20'
        props: BaseArticleModel = load_model(dn, BaseArticleModel, yaml)
        assert 20 == props.weight

    def test_article_missing(self):
        dn = 'index'
        yaml = 'weight: 20'
        with pytest.raises(SphinxError) as excinfo:
            load_model(dn, BaseWidgetModel, yaml)
        assert 'Validation error in docname index' in str(excinfo.value)

    def test_article_extra(self):
        dn = 'index'
        yaml = 'flag: 9'
        with pytest.raises(SphinxError) as excinfo:
            load_model(dn, BaseWidgetModel, yaml)
        assert 'Validation error in docname index' in str(excinfo.value)

