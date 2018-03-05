from kaybee.app import kb

from kaybee.plugins.references.base_reference import BaseReference
from kaybee.plugins.resources.base_resource import BaseResource


@kb.resource('indexpage')
class Indexpage(BaseResource):
    pass


@kb.resource('author')
class Author(BaseReference):
    pass
