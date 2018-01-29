from kaybee.app import kb

from kaybee.plugins.resources.base_resource import (
    BaseResource,
    BaseResourceModel
)
from kaybee.plugins.references.model_types import ReferencesType


class IndexpageModel(BaseResourceModel):
    reference: ReferencesType = []


@kb.resource('indexpage')
class Indexpage(BaseResource):
    props: IndexpageModel
