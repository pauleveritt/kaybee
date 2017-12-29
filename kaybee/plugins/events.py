"""

Dectate action to manage event callbacks in the configuration.

"""
import dectate


class EventAction(dectate.Action):
    _sphinx_event_names = [
        'builder-init',
        'env-purge-doc',
        'env-before-read-docs',
        'doctree-read',
        'doctree-resolved',
        'missing-reference',
        'html-collect-pages',
        'env-check-consistency',
        'html-context'
    ]
    config = {
        'events': dict
    }

    def __init__(self, name, scope):
        assert name in self._sphinx_event_names
        super().__init__()
        self.name = name
        self.scope = scope

    def identifier(self, events):
        return self.name + '-' + self.scope

    def perform(self, obj, events):
        events[self.name] = obj

    @classmethod
    def get_callbacks(cls, registry, event_name: str):
        # Presumes the registry has been committed

        # First ensure that event_name is valid
        assert event_name in cls._sphinx_event_names

        q = dectate.Query('event')
        return [args[1] for args in q(registry) if args[0].name == event_name]

    # Dispatchers for each of the Sphinx methods
    @classmethod
    def call_builder_init(cls, kb_app, sphinx_app):
        """ On builder init event, commit registry and do callbacks """

        dectate.commit(kb_app)
        for callback in cls.get_callbacks(kb_app, 'builder-init'):
            callback(kb_app, sphinx_app)
