from kaybee.app import kb
from kaybee.plugins.widgets.base_widget import (
    BaseWidget,
    BaseWidgetModel,
)


class SectionboxModel(BaseWidgetModel):
    heading: str = None
    subheading: str = None
    style: str = None


@kb.widget('sectionbox')
class SectionboxWidget(BaseWidget):
    props: SectionboxModel
