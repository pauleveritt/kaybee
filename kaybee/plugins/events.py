"""

Dectate action to manage event callbacks in the configuration.

"""

from enum import Enum
from typing import List

from docutils.readers import doctree
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment

import dectate


class SphinxEvent(Enum):
    BI = 'builder-inited'
    EPD = 'env-purge-doc'
    EBRD = 'env-before-read-docs'
    DREAD = 'doctree-read'
    DRES = 'doctree-resolved'
    MR = 'missing-reference'
    HCP = 'html-collect-pages'
    ECC = 'env-check-consistency'
    HC = 'html-context'


class EventAction(dectate.Action):
    config = {
        'events': dict
    }

    def __init__(self, name, scope):
        assert name in SphinxEvent
        super().__init__()
        self.name = name
        self.scope = scope

    def identifier(self, events):
        return self.name.value + '-' + self.scope

    # noinspection PyMethodOverriding
    def perform(self, obj, events):
        events[self.name] = obj

    @classmethod
    def get_callbacks(cls, registry, event_name: SphinxEvent):
        # Presumes the registry has been committed

        # First ensure that event_name is valid
        assert event_name in SphinxEvent

        q = dectate.Query('event')
        return [args[1] for args in q(registry) if args[0].name == event_name]

    #
    # Dispatchers for each of the Sphinx methods
    #
    @classmethod
    def call_builder_init(cls, kb_app, sphinx_app: Sphinx):
        """ On builder init event, commit registry and do callbacks """

        dectate.commit(kb_app)
        for callback in cls.get_callbacks(kb_app, SphinxEvent.BI):
            callback(kb_app, sphinx_app)

    @classmethod
    def call_purge_doc(cls, kb_app, sphinx_app: Sphinx, env,
                       docname: str):
        """ On env-purge-doc, do callbacks """

        for callback in EventAction.get_callbacks(kb_app, SphinxEvent.EPD):
            callback(kb_app, sphinx_app, env, docname)

    @classmethod
    def call_env_before_read_docs(cls, kb_app, sphinx_app: Sphinx,
                                  env: BuildEnvironment,
                                  docnames: List[str]):
        """ On env-read-docs, do callbacks"""

        for callback in EventAction.get_callbacks(kb_app,
                                                  SphinxEvent.EBRD):
            callback(kb_app, sphinx_app, env, docnames)

    @classmethod
    def call_env_doctree_read(cls, kb_app, sphinx_app: Sphinx,
                              doctree: doctree):
        """ On doctree-read, do callbacks"""

        for callback in EventAction.get_callbacks(kb_app,
                                                  SphinxEvent.DREAD):
            callback(kb_app, sphinx_app, doctree)

    @classmethod
    def call_doctree_resolved(cls, kb_app, sphinx_app: Sphinx,
                              doctree: doctree,
                              fromdocname: str):
        """ On doctree-resolved, do callbacks"""

        for callback in EventAction.get_callbacks(kb_app,
                                                  SphinxEvent.DREAD):
            callback(kb_app, sphinx_app, doctree)
