"""

Widget providing a number of queries to be performed then laid out
in columns.

"""
from typing import Dict

from kaybee.app import kb
from kaybee.plugins.queries.props_model import BaseQueryModel
from kaybee.plugins.queries.service import Query
from kaybee.plugins.widgets.base_widget import (
    BaseWidget,
    BaseWidgetModel,
)


class SectionqueryModel(BaseWidgetModel):
    query: BaseQueryModel


@kb.widget('sectionquery')
class SectionqueryWidget(BaseWidget):
    props: SectionqueryModel

    def make_context(self, context: Dict, sphinx_app):
        """ Put information into the context for rendering """

        query = self.props.query
        results = Query.filter_collection(
            sphinx_app.env.resources,
            rtype=query.rtype,
            props=query.props,
            parent_name=query.parent_name,
            sort_value=query.sort_value,
            limit=query.limit,
            reverse=query.reverse
        )
        context['results'] = results
        context['result_count'] = len(results)
