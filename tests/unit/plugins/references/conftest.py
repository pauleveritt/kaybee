import dectate
import pytest


@pytest.fixture()
def references_sphinx_app(sphinx_app):
    sphinx_app.references = dict()

    yield sphinx_app


@pytest.fixture()
def conflicting_registrations(kb_app):
    # Omit the "order" to disambiguate
    @kb_app.reference('category')
    def category1(*args):
        return

    @kb_app.reference('category')
    def category2(*args):
        return

    yield (category1, category2)


@pytest.fixture()
def valid_registration(kb_app):
    @kb_app.reference('category')
    def category1(*args):
        return

    dectate.commit(kb_app)
    yield category1

