"""

An out-of-the-box widget type.

This can be used in RST with something like::

   .. widget::
      name: someuniquename
      template: sometemplate.html

"""
from typing import Mapping

from sphinx.application import Sphinx

from kaybee.app import kb

from kaybee.plugins.widgets.base_widget import BaseWidget


@kb.widget('widget')
class Widget(BaseWidget):
    def make_context(self, context: Mapping, sphinx_app: Sphinx):
        pass
