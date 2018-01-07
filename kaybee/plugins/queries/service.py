from operator import attrgetter
from typing import List, Dict

import pydash


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

        # Start with (hopefully) most common, filter based on resource type
        r1 = pydash.filter_(collection, Query._attr_lambda('rtype', rtype))

        # Filter those results based on arbitrary key-value pairs
        for prop in props:
            r1 = pydash.filter_(collection,
                                Query._prop_lambda(prop['key'], prop['value']))

        # Filter out only those with a parent in their lineage
        # TODO this only works with resources
        r1 = pydash.filter_(r1,
                            Query._filter_parents(collection, parent_name))

        # Apply the "is_published" filter, if present
        if is_published:
            r1 = pydash.filter_(r1, lambda x: x.is_published())

        # Now sorting
        r1 = pydash.sort_by(r1,
                            Query._sort_key_lamda(sort_value),
                            reverse=reverse
                            )
        r1 = r1[:limit]

        return r1
