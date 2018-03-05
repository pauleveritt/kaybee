import dectate
import pytest
from pydantic import BaseModel

from kaybee.plugins.references.base_reference import BaseReference
from kaybee.plugins.references.container import ReferencesContainer
from kaybee.plugins.references.model_types import ReferencesType
from kaybee.plugins.resources.action import ResourceAction
from kaybee.plugins.resources.base_resource import (
    BaseResource,
    BaseResourceModel,
)


class DummyArticleModel(BaseModel):
    reference: ReferencesType = []


class DummyResource(BaseResource):
    props: BaseResourceModel


class DummyReference(BaseReference):
    is_reference = True


class DummyReferences(ReferencesContainer):
    pass


@pytest.fixture()
def references_kb_app():
    class references_kb_app(dectate.App):
        resource = dectate.directive(ResourceAction)

    yield references_kb_app


@pytest.fixture()
def dummy_resource():
    yaml_content = '''\
references:
    reference: [reference1]
    '''
    yield DummyResource('resource1', 'resource', yaml_content)


@pytest.fixture()
def dummy_reference():
    yaml_content = '''\
label: reference1
    '''
    dc = DummyReference('reference1', 'reference', yaml_content)
    dc.title = 'Dummy Reference 1'
    yield dc


@pytest.fixture()
def references_sphinx_app(sphinx_app, references_sphinx_env):
    sphinx_app.env = references_sphinx_env

    yield sphinx_app


@pytest.fixture()
def references_sphinx_env(sphinx_env, dummy_resource, dummy_reference):
    sphinx_env.references = DummyReferences()
    sphinx_env.references['reference'] = dict(
        reference1=dummy_reference
    )
    sphinx_env.resources = dict(
        resource1=dummy_resource
    )
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
    @references_kb_app.resource('reference')
    class Reference11(BaseReference):
        pass

    @references_kb_app.resource('reference')
    class Reference2(BaseReference):
        pass

    yield (Reference11, Reference2)


@pytest.fixture()
def valid_registration(references_kb_app):
    @references_kb_app.resource('reference')
    class Reference1(BaseReference):
        pass

    dectate.commit(references_kb_app)
    yield Reference1
