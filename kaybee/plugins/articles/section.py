"""

An out-of-the-box section type.

This can be used in RST with something like::

   .. section::
      template: section.html

"""

from kaybee.app import kb

from kaybee.plugins.articles.base_section import BaseSection


@kb.resource('section')
class Section(BaseSection):
    pass
