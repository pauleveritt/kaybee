"""

A UserDict container for resources.

This allows us to validate schemas on add plus provide some query-like
methods on the app.resources instance

"""
from collections import UserDict


class ResourcesContainer(UserDict):
    def __setitem__(self, name, value):
        self.data[name] = value
