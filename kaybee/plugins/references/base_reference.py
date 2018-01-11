from kaybee.plugins.resources.base_resource import (
    BaseResource,
    BaseResourceModel
)


class BaseReferenceModel(BaseResourceModel):
    label: str


class BaseReference(BaseResource):
    model = BaseReferenceModel
    is_reference = True
