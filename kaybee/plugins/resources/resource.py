"""

An out-of-the-box resource type.

This can be used in RST with something like::

   .. resource::
      template: sometemplate.html

"""

from kaybee.app import kb

from kaybee.plugins.resources.base_resource import BaseResource


@kb.resource('resource')
class Resource(BaseResource):
    pass
