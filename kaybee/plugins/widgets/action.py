"""

An action for the kb registry app.

"""

import dectate


class WidgetAction(dectate.Action):
    config = {
        'widgets': dict
    }

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def identifier(self, widgets):
        return self.name

    # noinspection PyMethodOverriding
    def perform(self, obj, widgets):
        widgets[self.name] = obj

    @classmethod
    def get_callbacks(cls, registry):
        # Presumes the registry has been committed

        q = dectate.Query('widget')
        return [args[1] for args in q(registry)]
