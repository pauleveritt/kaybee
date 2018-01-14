"""

Actions for the kb registry app.

"""
from typing import Optional

import dectate


class ToctreeAction(dectate.Action):
    config = {
        'toctrees': dict
    }

    def __init__(self, context: Optional[str] = None,
                 system_order: Optional[int] = 80):
        super().__init__()
        self.context = context
        self.system_order = system_order

    def identifier(self, toctrees):
        return f'{self.context}-{self.system_order}'

    # noinspection PyMethodOverriding
    def perform(self, obj, toctrees):
        name = f'{self.context}-{self.system_order}'
        toctrees[name] = obj

    @classmethod
    def get_callbacks(cls, registry):
        # Presumes the registry has been committed

        q = dectate.Query('toctree')
        return [args[1] for args in q(registry)]

    @classmethod
    def get_for_context(cls, registry, context=None):
        q = dectate.Query('toctree')
        # Get the registrations for this context, sorted by
        # system_order
        qr = sorted(
            q.filter(context=context)(registry),
            key=lambda t: t[0].system_order
        )
        # Return the first match's decorated object
        return qr[0][1]
