"""

Actions for the kb registry app.

"""
from typing import Optional

import dectate


class ToctreeAction(dectate.Action):
    config = {
        'toctrees': dict
    }

    def __init__(self, context: Optional[str] = None):
        super().__init__()
        self.context = context

    def identifier(self, toctrees):
        return self.context

    # noinspection PyMethodOverriding
    def perform(self, obj, toctrees):
        toctrees[self.context] = obj

    @classmethod
    def get_callbacks(cls, registry):
        # Presumes the registry has been committed

        q = dectate.Query('toctree')
        return [args[1] for args in q(registry)]

    @classmethod
    def get_for_context(cls, registry, context=None):
        q = dectate.Query('toctree')
        qr = list(q.filter(context=context)(registry))
        # Return the first match's decorated object
        return qr[0][1]
