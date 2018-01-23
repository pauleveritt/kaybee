"""

An out-of-the-box reference type.

This can be used in RST with something like::

   .. reference::
      template: sometemplate.html

"""

from kaybee.app import kb

from kaybee.plugins.references.base_reference import BaseReference


@kb.resource('reference')
class Reference(BaseReference):
    pass
