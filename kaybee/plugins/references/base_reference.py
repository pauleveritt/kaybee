from kaybee.plugins.resources.base_resource import (
    BaseResource,
    BaseResourceModel
)


def is_reference_target(resource, rtype, label):
    """ Return true if the resource has this rtype with this label """

    prop = resource.props.references.get(rtype, False)
    if prop:
        return label in prop


class BaseReferenceModel(BaseResourceModel):
    label: str


class BaseReference(BaseResource):
    props: BaseReferenceModel
    is_reference = True

    def get_sources(self, resources):
        """ Filter resources based on which have this reference """

        rtype = self.rtype  # E.g. category
        label = self.props.label  # E.g. category1
        result = [
            resource
            for resource in resources.values()
            if is_reference_target(resource, rtype, label)
        ]
        return result
