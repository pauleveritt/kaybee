from operator import attrgetter
from typing import List, Dict, Optional

import pydash
from pydash import py_

from kaybee.plugins.queries.props_model import CorePropFilterModel


class Query:
    def __init__(self, docname):
        self.docname = docname

    @classmethod
    def _attr_lambda(cls, key, value):
        # For use in filter expressions. If the value is None, then
        # don't do any filtering. If the value is not None, then we need
        # to filter.
        if value is None:
            return lambda x: True
        else:
            return lambda x: getattr(x, key, None) == value

    @classmethod
    def _prop_lambda(cls, key, value):
        # For use in filter expressions. If the value is None, then
        # don't do any filtering. If the value is not None, then we need
        # to filter.
        if value is None:
            return lambda x: True
        else:
            return lambda x: getattr(x.props, key, None) == value

    @classmethod
    def _filter_parents(cls, collection, parent_name):
        if parent_name is None:
            return lambda x: True
        else:
            return lambda x: collection[parent_name] in x.parents(collection)

    @classmethod
    def _sort_key_lamda(cls, sort_value):
        if sort_value is None:
            # The dummy user explicity said to sort on nothing. What to
            # sort on then, when they don't want the default sort_value of
            # 'title' ? For now, docname
            return attrgetter('docname')
        elif sort_value == 'title':
            return attrgetter('title')
        else:
            def get_prop(resource):
                prop = getattr(resource.props, sort_value, None)
                if prop is None:
                    return ''
                else:
                    return prop
            return get_prop

    @classmethod
    def filter_collection(self,
                          collection,
                          rtype: str = None,
                          sort_value: Optional[str] = 'title',
                          reverse: bool = False,
                          limit: int = None,
                          parent_name: str = None,
                          props: List[CorePropFilterModel] = [],
                          ):

        # Set the limit
        if limit is None:
            limit = len(collection.values())

        # Filter those results based on arbitrary key-value pairs
        r1 = collection
        for prop in props:
            r1 = pydash.filter_(r1,
                                Query._prop_lambda(prop.key, prop.value))

        r1 = py_(r1) \
            .filter_(Query._attr_lambda('rtype', rtype)) \
            .filter_(Query._filter_parents(collection, parent_name)) \
            .sort_by(Query._sort_key_lamda(sort_value),
                     reverse=reverse
                     ) \
            .slice(0, limit)

        return r1.value()
