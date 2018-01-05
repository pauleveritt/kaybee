"""

An action for the kb registry app.

"""

import dectate

from kaybee.plugins.genericpage.genericpage import Genericpage


class GenericpageAction(dectate.Action):
    config = {
        'genericpages': dict
    }

    def __init__(self, order: int = 40):
        #
        # TODO
        # - can you acquire a prop that isn't in your schema, just hangs
        #   off of acquires?
        super().__init__()
        self.order = order

    def identifier(self, genericpages):
        return str(self.order)

    # noinspection PyMethodOverriding
    def perform(self, obj, genericpages):
        genericpages[self.order] = obj

    @classmethod
    def get_genericpage(cls, registry):
        """ Return the one class if configured, otherwise default """

        # Presumes the registry has been committed
        q = dectate.Query('genericpage')
        klasses = sorted(q(registry), key=lambda args: args[0].order)
        if not klasses:
            # The site doesn't configure a genericpage,
            return Genericpage
        else:
            return klasses[0][1]
