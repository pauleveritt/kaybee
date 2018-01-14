"""

An out-of-the-box homepage type.

This can be used in RST with something like::

   .. homepage::
      template: sometemplate.html

"""

from kaybee.app import kb

from kaybee.plugins.articles.base_homepage import BaseHomepage


@kb.resource('homepage')
class Homepage(BaseHomepage):
    pass
