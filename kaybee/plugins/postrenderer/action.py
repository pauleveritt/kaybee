"""

An action for the postrenderers to register against.

"""

import dectate


class PostrendererAction(dectate.Action):
    config = {
        'postrenderers': dict
    }

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def identifier(self, postrenderers):
        return self.name

    # noinspection PyMethodOverriding
    def perform(self, obj, postrenderers):
        postrenderers[self.name] = obj

    @classmethod
    def get_callbacks(cls, registry):
        # Presumes the registry has been committed

        q = dectate.Query('postrenderer')
        return [args[1] for args in q(registry)]
