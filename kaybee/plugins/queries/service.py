from operator import attrgetter
from typing import List, Dict

import pydash
from pydash import py_


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
            return None
        elif sort_value == 'title':
            return attrgetter('title')
        else:
            return lambda x: getattr(x.props, sort_value, 0)

    @classmethod
    def filter_collection(self,
                          collection,
                          rtype: str = None,
                          sort_value: str = 'title',
                          reverse: bool = False,
                          limit: int = None,
                          parent_name: str = None,
                          props: List[Dict[str, str]] = [],
                          is_published=False):

        # Set the limit
        if limit is None:
            limit = len(collection.values())

        # Filter those results based on arbitrary key-value pairs
        r1 = collection
        for prop in props:
            r1 = pydash.filter_(r1,
                                Query._prop_lambda(prop['key'], prop['value']))

        # Start with (hopefully) most common, filter based on resource type
        r1 = py_(r1) \
            .filter_(Query._attr_lambda('rtype', rtype)) \
            .filter_(Query._filter_parents(collection, parent_name)) \
            .sort_by(Query._sort_key_lamda(sort_value),
                     reverse=reverse
                     ) \
            .slice(0, limit)

        return r1.value()
