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

    # noinspection PyMethodOverriding
    def perform(self, obj, events):
        events[self.name] = obj

    @classmethod
    def get_callbacks(cls, registry, event_name: str):
        # Presumes the registry has been committed

        # First ensure that event_name is valid
        assert event_name in cls._sphinx_event_names

        q = dectate.Query('event')
        return [args[1] for args in q(registry) if args[0].name == event_name]

    #
    # Dispatchers for each of the Sphinx methods
    #
    @classmethod
    def call_builder_init(cls, kb_app, sphinx_app):
        """ On builder init event, commit registry and do callbacks """

        dectate.commit(kb_app)
        for callback in cls.get_callbacks(kb_app, 'builder-init'):
            callback(kb_app, sphinx_app)

    @classmethod
    def call_purge_doc(cls, kb_app, sphinx_app, env, docname):
        """ On env-purge-doc, do callbacks """

        for callback in EventAction.get_callbacks(kb_app, 'env-purge-doc'):
            callback(kb_app, sphinx_app, env, docname)

    @classmethod
    def call_env_before_read_docs(cls, kb_app, sphinx_app, env, docnames):
        """ On env-read-docs, do callbacks"""

        for callback in EventAction.get_callbacks(kb_app,
                                                  'env-before-read-docs'):
            callback(kb_app, sphinx_app, env, docnames)

        # if not hasattr(env, 'site'):
        #     config = getattr(app.config, 'kaybee_config')
        #     if config:
        #         env.site = Site(config)
        #
        # template_bridge = app.builder.templates
        #
        # # Add _templates in the conf directory
        # confdir = os.path.join(app.confdir, '_templates')
        # template_bridge.loaders.append(SphinxFileSystemLoader(confdir))
        #
        # for callback in EventAction.get_callbacks(kb,
        # 'env-before-read-docs'):
        #     callback(kb, app, env, docnames)
