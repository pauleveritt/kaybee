from sphinx.application import Sphinx

from kaybee.app import kb
from kaybee.plugins.widgets.base_widget import (
    BaseWidget,
    BaseWidgetModel,
)


class ListingModel(BaseWidgetModel):
    listing_flag: int


@kb.widget('listing')
class ListingWidget(BaseWidget):
    greeting = 'widget greeting'

    def make_context(self, context, sphinx_app: Sphinx):
        context['another_flag'] = 835
