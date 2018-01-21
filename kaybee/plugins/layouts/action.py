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
    def get_layout(cls, kb_app, theme_name):
        """ Return  layout class pointed to by sphinx_app's html_theme """

        q = dectate.Query('layout')
        klasses = list(q.filter(name=theme_name)(kb_app))
        if klasses:
            return klasses[0][1]
        else:
            msg = f'No registered layout named {theme_name}'
            raise KeyError(msg)
