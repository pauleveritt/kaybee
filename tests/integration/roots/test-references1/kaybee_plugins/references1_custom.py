from kaybee.app import kb

from kaybee.plugins.references.base_reference import BaseReference
from kaybee.plugins.references.model_types import ReferencesType
from kaybee.plugins.resources.base_resource import (
    BaseResource,
    BaseResourceModel
)


class IndexpageModel(BaseResourceModel):
    reference: ReferencesType = []


@kb.resource('indexpage')
class Indexpage(BaseResource):
    props: IndexpageModel


@kb.resource('author')
class Author(BaseReference):
    pass
