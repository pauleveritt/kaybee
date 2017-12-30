"""

An action for the kb registry app.

"""

import dectate


class DumperAction(dectate.Action):
    config = {
        'dumpers': dict
    }

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def identifier(self, dumpers):
        return self.name

    # noinspection PyMethodOverriding
    def perform(self, obj, dumpers):
        dumpers[self.name] = obj

    @classmethod
    def get_callbacks(cls, registry):
        # Presumes the registry has been committed

        q = dectate.Query('dumper')
        return [args[1] for args in q(registry)]
