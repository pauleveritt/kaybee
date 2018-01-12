import dectate
import pytest

from kaybee.plugins.references.base_reference import BaseReference


class DummyProps:
    pass


class DummyArticle:
    def __init__(self, docname):
        self.docname = docname
        self.props = DummyProps()
        self.props.category = ('category1',)
        self.reference_fieldnames = ('category',)


class DummyCategory:
    def __init__(self, docname):
        self.docname = docname
        self.props = DummyProps()


class DummyReferences(dict):
    def get_reference(self):
        pass


@pytest.fixture()
def references_sphinx_app(sphinx_app):
    article1 = DummyArticle('article1')
    category1 = DummyCategory('category1')
    sphinx_app.references = DummyReferences()
    sphinx_app.references['category'] = dict(
        category1=category1
    )
    sphinx_app.resources = dict(
        article1=article1
    )

    yield sphinx_app


@pytest.fixture()
def conflicting_registrations(kb_app):
    # Omit the "order" to disambiguate
    @kb_app.reference('category')
    class Category1(BaseReference):
        pass

    @kb_app.reference('category')
    class Category2(BaseReference):
        pass

    yield (Category1, Category2)


@pytest.fixture()
def valid_registration(kb_app):
    @kb_app.reference('category')
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
