"""

Widget providing a number of queries to be performed then laid out
in columns.

"""
from typing import Dict, List

from pydantic import BaseModel

from kaybee.app import kb
from kaybee.plugins.queries.props_model import BaseQueryModel
from kaybee.plugins.queries.service import Query
from kaybee.plugins.widgets.base_widget import (
    BaseWidget,
    BaseWidgetModel,
)


class FeatureTile(BaseModel):
    style: str = ''
    heading: str
    subheading: str = None
    bullets: List[str] = None
    more_href: str = None


class FeaturetilesModel(BaseWidgetModel):
    rows: List[List[FeatureTile]] = []


@kb.widget('featuretiles')
class FeaturetilesWidget(BaseWidget):
    props: FeaturetilesModel
