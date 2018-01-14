"""

Dectate action to manage event callbacks in the configuration.

"""

import importlib
import os
import sys
from enum import Enum
from typing import List

import dectate
import importscan
from docutils.readers import doctree
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment
from sphinx.util import logging

logger = logging.getLogger(__name__)


class SphinxEvent(Enum):
    BI = 'builder-inited'
    EPD = 'env-purge-doc'
    EBRD = 'env-before-read-docs'
    DREAD = 'doctree-read'
    DRES = 'doctree-resolved'
    MR = 'missing-reference'
    HCP = 'html-collect-pages'
    EU = 'env-updated'
    ECC = 'env-check-consistency'
    HPC = 'html-page-context'


class EventAction(dectate.Action):
    config = {
        'events': dict
    }

    def __init__(self,
                 name: str,
                 order: int = 20,
                 scope=None,
                 system_order=None):
        assert name in SphinxEvent
        super().__init__()
        self.name = name
        self.scope = scope

        if system_order is None:
            # This is a user handler
            # 40 to 80 is reserved for system handlers.
            assert order < 40 or order > 80
            self.order = order
        else:
            assert 40 <= system_order <= 80
            self.order = system_order

    def identifier(self, events):
        if self.scope:
            return f'{self.name.value}-{self.scope}-{self.order}'
        else:
            return f'{self.name.value}-{self.order}'

    # noinspection PyMethodOverriding
    def perform(self, obj, events):
        events[self.name] = obj

    @classmethod
    def get_callbacks(cls, registry, event_name: SphinxEvent):
        # Presumes the registry has been committed

        # First ensure that event_name is valid
        assert event_name in SphinxEvent

        q = dectate.Query('event')
        qr = sorted(q(registry), key=lambda args: args[0].order)
        return [args[1] for args in qr if args[0].name == event_name]

    #
    # Dispatchers for each of the Sphinx methods
    #
    @classmethod
    def call_builder_init(cls, kb_app, sphinx_app: Sphinx):
        """ On builder init event, commit registry and do callbacks """

        # Find and commit docs project plugins
        conf_dir = sphinx_app.confdir
        plugins_dir = sphinx_app.config.kaybee_settings.plugins_dir
        full_plugins_dir = os.path.join(conf_dir, plugins_dir)

        if os.path.exists(full_plugins_dir):
            sys.path.insert(0, conf_dir)
            plugin_package = importlib.import_module(plugins_dir)
            importscan.scan(plugin_package)
        else:
            logger.info(f'## Kaybee: No plugin dir at {plugins_dir}')

        dectate.commit(kb_app)
        for callback in cls.get_callbacks(kb_app, SphinxEvent.BI):
            callback(kb_app, sphinx_app)

    @classmethod
    def call_purge_doc(cls, kb_app, sphinx_app: Sphinx,
                       sphinx_env: BuildEnvironment,
                       docname: str):
        """ On env-purge-doc, do callbacks """

        for callback in EventAction.get_callbacks(kb_app, SphinxEvent.EPD):
            callback(kb_app, sphinx_app, sphinx_env, docname)

    @classmethod
    def call_env_before_read_docs(cls, kb_app, sphinx_app: Sphinx,
                                  sphinx_env: BuildEnvironment,
                                  docnames: List[str]):
        """ On env-read-docs, do callbacks"""

        for callback in EventAction.get_callbacks(kb_app,
                                                  SphinxEvent.EBRD):
            callback(kb_app, sphinx_app, sphinx_env, docnames)

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
                                                  SphinxEvent.DRES):
            callback(kb_app, sphinx_app, doctree, fromdocname)

    @classmethod
    def call_env_updated(cls, kb_app,
                         sphinx_app: Sphinx,
                         sphinx_env: BuildEnvironment):

        """ On the env-updated event, do callbacks """
        for callback in EventAction.get_callbacks(kb_app, SphinxEvent.EU):
            callback(kb_app, sphinx_app, sphinx_env)

    @classmethod
    def call_html_collect_pages(cls, kb_app, sphinx_app: Sphinx):
        """ On html-collect-pages, do callbacks"""

        EventAction.get_callbacks(kb_app,
                                  SphinxEvent.HCP)
        for callback in EventAction.get_callbacks(kb_app,
                                                  SphinxEvent.HCP):
            yield callback(kb_app, sphinx_app)

    @classmethod
    def call_env_check_consistency(cls, kb_app, builder: StandaloneHTMLBuilder,
                                   sphinx_env: BuildEnvironment):
        """ On env-check-consistency, do callbacks"""

        for callback in EventAction.get_callbacks(kb_app,
                                                  SphinxEvent.ECC):
            callback(kb_app, builder, sphinx_env)

    @classmethod
    def call_missing_reference(cls, kb_app, sphinx_app: Sphinx,
                               sphinx_env: BuildEnvironment,
                               node,
                               contnode,
                               ):
        """ On doctree-resolved, do callbacks"""

        for callback in EventAction.get_callbacks(kb_app,
                                                  SphinxEvent.MR):
            return callback(kb_app, sphinx_app, sphinx_env, node, contnode)

    @classmethod
    def call_html_page_context(cls, kb_app, sphinx_app: Sphinx,
                               pagename: str,
                               templatename: str,
                               context,
                               doctree: doctree
                               ):
        """ On doctree-resolved, do callbacks"""

        # We need to let one, and only one, callback return the name of
        # the template. Detect multiple and raise an exception.
        new_templatename = None

        for callback in EventAction.get_callbacks(kb_app,
                                                  SphinxEvent.HPC):
            # The protocol: the one controlling callback will return a value
            # with a dictionary of {'templatename': 'sometemplate'}
            result = callback(kb_app, sphinx_app, pagename, templatename,
                              context,
                              doctree)
            if result and isinstance(result,
                                     dict) and 'templatename' in result:
                if new_templatename is not None:
                    raise AssertionError('Multiple handlers returning')
                new_templatename = result['templatename']

        return new_templatename
