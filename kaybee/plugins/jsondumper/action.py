"""

An action for the kb registry app.

"""

import dectate


class JsondumperAction(dectate.Action):
    config = {
        'jsondumpers': dict
    }

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def identifier(self, jsondumpers):
        return self.name

    # noinspection PyMethodOverriding
    def perform(self, obj, jsondumpers):
        jsondumpers[self.name] = obj

    @classmethod
    def get_callbacks(cls, registry):
        # Presumes the registry has been committed

        q = dectate.Query('jsondumper')
        return [args[1] for args in q(registry)]
