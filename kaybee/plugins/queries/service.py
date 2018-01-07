from operator import attrgetter
from typing import List, Dict

# import pydash


class Query:
    def __init__(self, docname):
        self.docname = docname

    @classmethod
    def filter_collection(self,
                          collection,
                          rtype: str = None,
                          sort_value: str = 'title',
                          order: int = 1,
                          limit: int = 5,
                          parent_name: str = None,
                          props: List[Dict[str, str]] = [],
                          is_published=False):

        # Start with (hopefully) most common, filter based on resource type
        if rtype:
            r1 = [r for r in collection.values() if r.rtype == rtype]
        else:
            r1 = list(collection.values())

        # Filter those results based on arbitrary key-value pairs
        for prop in props:
            r1 = [r for r in r1
                  if getattr(r.props, prop['key'], None) == prop['value']]

        # Filter out only those with a parent in their lineage
        # TODO this only works with resources
        if parent_name:
            parent = collection[parent_name]
            r2 = [r for r in r1 if parent in r.parents(collection)]
        else:
            r2 = r1

        # Apply the "is_published" filter, if present
        if is_published:
            r2 = [resource for resource in r2 if resource.is_published()]

        # Now sorting
        if sort_value:
            if sort_value == 'title':
                # Special case, everything else is in props
                r3 = sorted(
                    r2,
                    key=attrgetter('title')
                )
            else:
                r3 = sorted(
                    r2,
                    key=lambda x:  getattr(x.props, sort_value, 0)
                )
        else:
            r3 = r2

        # Reverse if needed
        if order == -1:
            r3.reverse()

        # Return a limited number
        if limit:
            r3 = r3[:limit]

        return r3
