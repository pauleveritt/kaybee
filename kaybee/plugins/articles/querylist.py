"""

Widget providing a number of queries to be performed then laid out
in columns.

"""
from typing import List

from pydantic import BaseModel

from kaybee.app import kb
from kaybee.plugins.queries.props_model import BaseQueryModel
from kaybee.plugins.widgets.base_widget import (
    BaseWidget,
    BaseWidgetModel,
)
from kaybee.plugins.queries.service import Query


class QuerySectionModel(BaseModel):
    label: str
    style: str = None
    query: BaseQueryModel


class QuerylistModel(BaseWidgetModel):
    queries: List[QuerySectionModel]


@kb.widget('querylist')
class QuerylistWidget(BaseWidget):
    props: QuerylistModel

    def make_context(self, context, sphinx_app):
        result_sets = []
        for query_section in self.props.queries:
            result_set = dict(
                label=query_section.label,
                style=query_section.style,
            )
            query = query_section.query
            results = Query.filter_collection(
                sphinx_app.env.resources,
                rtype=query.rtype,
                props=query.props,
                parent_name=query.parent_name,
                sort_value=query.sort_value,
                limit=query.limit,
                reverse=query.reverse
            )
            result_set['results'] = results
            result_sets.append(result_set)

        context['result_sets'] = result_sets
