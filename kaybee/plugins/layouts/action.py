"""

Actions for the kb registry app.

"""
from typing import Optional

import dectate


class LayoutAction(dectate.Action):
    config = {
        'layouts': dict
    }

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def identifier(self, layouts):
        return self.name

    # noinspection PyMethodOverriding
    def perform(self, obj, layouts):
        layouts[self.name] = obj

    @classmethod
    def get_callbacks(cls, registry):
        q = dectate.Query('layout')
        return [args[1] for args in q(registry)]

    @classmethod
    def get_layout(cls, kb_app, layout_name):
        """ Return  layout class pointed to by the name """

        q = dectate.Query('layout')
        klasses = list(q.filter(name=layout_name)(kb_app))
        if klasses:
            return klasses[0][1]
        else:
            msg = f'No registered layout named {layout_name}'
            raise KeyError(msg)
