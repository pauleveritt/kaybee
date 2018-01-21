import dectate
import pytest
from pydantic import BaseModel

from kaybee.plugins.references.base_reference import BaseReference
from kaybee.plugins.references.container import ReferencesContainer
from kaybee.plugins.references.model_types import ReferencesType
from kaybee.plugins.resources.action import ResourceAction
from kaybee.plugins.resources.base_resource import BaseResource


class DummyArticleModel(BaseModel):
    category: ReferencesType = []


class DummyArticle(BaseResource):
    model = DummyArticleModel


class DummyCategory(BaseReference):
    is_reference = True


class DummyReferences(ReferencesContainer):
    pass


@pytest.fixture()
def references_kb_app():
    class references_kb_app(dectate.App):
        resource = dectate.directive(ResourceAction)

    yield references_kb_app


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
    dc = DummyCategory('category1', 'category', yaml_content)
    dc.title = 'Dummy Category 1'
    yield dc


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
def references_sphinx_env(sphinx_env, references_sphinx_app):
    sphinx_env.app = references_sphinx_app

    yield sphinx_env


@pytest.fixture()
def dummy_contnode():
    class ContNode:
        def __init__(self):
            self.children = ('first',)

    yield ContNode()


@pytest.fixture()
def conflicting_registrations(references_kb_app):
    # Omit the "order" to disambiguate
    @references_kb_app.resource('category')
    class Category1(BaseReference):
        pass

    @references_kb_app.resource('category')
    class Category2(BaseReference):
        pass

    yield (Category1, Category2)


@pytest.fixture()
def valid_registration(references_kb_app):
    @references_kb_app.resource('category')
    class Category1(BaseReference):
        pass

    dectate.commit(references_kb_app)
    yield Category1
