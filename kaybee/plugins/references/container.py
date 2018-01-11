"""

Managing the setting/retrieving of references via a UserDict.

Store/retrieve each as sphinx_app.references[rtype][label]

"""

from collections import UserDict


class ReferencesContainer(UserDict):

    def get_reference(self, rtype: str, label: str):
        """ Return reference filed under rtype/label

         The references are organized by field/label, e.g. category/cat1.
         This lets us use a shorthand notation to go the resource, e.g.
         ref:category:cat1 instead of folder1/folder2/cat1.
         """

        return self.data[rtype][label]

    def add_reference(self, rtype: str, label: str, target):
        """ Add reference object in references under rtype/label=target """

        # if rtype not in self.data:
        #     self.data[rtype] = dict()
        self.data[rtype][label] = target
