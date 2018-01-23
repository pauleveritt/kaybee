"""

Managing the setting/retrieving of references via a UserDict.

Store/retrieve each as sphinx_app.references[rtype][label]

"""

from collections import UserDict
from typing import List, Mapping, Any

from kaybee.plugins.references.model_types import ReferencesType


class ReferencesContainer(UserDict):

    def get_reference(self, rtype: str, label: str):
        """ Return reference filed under rtype/label

         The references are organized by field/label, e.g. category/cat1.
         This lets us use a shorthand notation to go the resource, e.g.
         ref:category:cat1 instead of folder1/folder2/cat1.
         """

        # We are doing this instead of dictionary access in case we change
        # the storage later to a multidict thingy for optimization.

        reftype = self.data.get(rtype)
        if reftype:
            # The reftype might be "python" or "sphinx" or something else
            # from an Intersphinx registry, not something internal to
            # Kaybee.
            return reftype[label]

    def add_reference(self, reftype: str, label: str, target):
        """ Add reference object in references under rtype/label=target """

        # The self.data[reftype] dict springs into being during the
        # register_references event handler at startup, which looks in the
        # kb registry for all registered reference names.
        self.data[reftype][label] = target

    def resource_references(self, resource) -> Mapping[str, List[Any]]:
        """ Resolve and return references

         Fields in resource.props can flag that they are references by
         using the references type. This method scans the model,
         finds any fields that are references, and returns the
         resources pointed to by those references.

         Note that we shouldn't get to the point of dangling references.
         Our custom Sphinx event should raise a references error
         during the build process (though maybe it is just a warning?)

         """

        references = dict()
        reference_fieldnames = [
            field.name
            for field in resource.props.fields.values()
            if field.type_ == ReferencesType
        ]

        for field_name in reference_fieldnames:
            references[field_name] = []

            # Iterate over each value on this field, e.g.
            # tags: tag1, tag2, tag3
            for target_label in getattr(resource.props, field_name):
                # Ask the site to get the object
                target = self.get_reference(field_name, target_label)
                references[field_name].append(target)

        return references
