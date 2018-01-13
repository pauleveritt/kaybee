import dectate
import pytest
from pydantic import BaseModel

from kaybee.plugins.references.base_reference import BaseReference
from kaybee.plugins.references.model_types import ReferencesType
from kaybee.plugins.resources.base_resource import BaseResource


class DummyArticleModel(BaseModel):
    category: ReferencesType = []


class DummyArticle(BaseResource):
    model = DummyArticleModel


class DummyCategory(BaseReference):
    pass


class DummyReferences(dict):
    def get_reference(self):
        pass


@pytest.fixture()
def dummy_article():
    yaml_content = '''\
category:
    - category1
    '''
    yield DummyArticle('article1', 'article', yaml_content)


@pytest.fixture()
def dummy_category():
    yaml_content = '''\
label: category1
    '''
    yield DummyCategory('category1', 'category', yaml_content)


@pytest.fixture()
def references_sphinx_app(sphinx_app, dummy_article, dummy_category):
    sphinx_app.references = DummyReferences()
    sphinx_app.references['category'] = dict(
        category1=dummy_category
    )
    sphinx_app.resources = dict(
        article1=dummy_article
    )

    yield sphinx_app


@pytest.fixture()
def conflicting_registrations(kb_app):
    # Omit the "order" to disambiguate
    @kb_app.resource('category')
    class Category1(BaseReference):
        pass

    @kb_app.resource('category')
    class Category2(BaseReference):
        pass

    yield (Category1, Category2)


@pytest.fixture()
def valid_registration(kb_app):
    @kb_app.resource('category')
    class Category1(BaseReference):
        pass

    dectate.commit(kb_app)
    yield Category1


@pytest.fixture()
def references_sphinx_env(sphinx_env, references_sphinx_app):
    sphinx_env.app = references_sphinx_app

    yield sphinx_env


@pytest.fixture()
def dummy_contnode():
    class ContNode:
        def __init__(self):
            self.children = ('first',)

    yield ContNode()
