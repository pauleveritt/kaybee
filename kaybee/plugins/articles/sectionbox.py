from kaybee.app import kb
from kaybee.plugins.widgets.base_widget import (
    BaseWidget,
    BaseWidgetModel,
)


class SectionboxModel(BaseWidgetModel):
    sectionbox_flag: int


@kb.widget('sectionbox')
class SectionboxWidget(BaseWidget):
    model = SectionboxModel
    greeting = 'widget greeting'

    def make_context(self, context, sphinx_app):
        context['another_flag'] = 835
