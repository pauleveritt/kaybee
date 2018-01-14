from kaybee.plugins.resources.base_resource import (
    BaseResource,
    BaseResourceModel
)


class BaseHomepageModel(BaseResourceModel):
    logo: str = None
    heading: str = None
    subheading: str = None
    hero_image: str = None


class BaseHomepage(BaseResource):
    model = BaseHomepageModel
