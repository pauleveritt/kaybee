from kaybee.plugins.resources.base_resource import (
    BaseResource,
    BaseResourceModel
)


class BaseHomepageModel(BaseResourceModel):
    pass


class BaseHomepage(BaseResource):
    model = BaseHomepageModel
