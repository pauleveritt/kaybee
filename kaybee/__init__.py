import dectate
import importscan
from sphinx.application import Sphinx

from kaybee import plugins
from kaybee.app import kb
from kaybee.plugins.events import EventAction, SphinxEvent
from kaybee.plugins.settings.model import KaybeeSettings

__version__ = '0.1.7'
__title__ = "kaybee"


def flush_everything(sphinx_app, sphinx_env):
    e = sphinx_app.env
    values = list(e.resources.values()) + list(e.genericpages.values())
    return [value.docname for value in values]


def setup(app: Sphinx):
    """ Initialize Kaybee as a Sphinx extension """

    # Scan for directives, first in the system, second in the docs project
    importscan.scan(plugins)
    dectate.commit(kb)

    app.add_config_value('kaybee_settings', KaybeeSettings(), 'html')
    bridge = 'kaybee.plugins.postrenderer.config.KaybeeBridge'
    app.config.template_bridge = bridge

    app.connect('env-updated', flush_everything)
    app.connect(SphinxEvent.BI.value,
                # pragma nocover
                lambda sphinx_app: EventAction.call_builder_init(
                    kb, sphinx_app)
                )
    app.connect(SphinxEvent.EPD.value,
                # pragma nocover
                lambda sphinx_app, sphinx_env,
                       docname: EventAction.call_purge_doc(
                    kb, sphinx_app, sphinx_env, docname)
                )

    app.connect(SphinxEvent.EBRD.value,
                # pragma nocover
                lambda sphinx_app, sphinx_env,
                       docnames: EventAction.call_env_before_read_docs(
                    kb, sphinx_app, sphinx_env, docnames)
                )

    app.connect(SphinxEvent.DREAD.value,
                # pragma nocover
                lambda sphinx_app,
                       doctree: EventAction.call_env_doctree_read(
                    kb, sphinx_app, doctree)
                )

    app.connect(SphinxEvent.DRES.value,
                # pragma nocover
                lambda sphinx_app, doctree,
                       fromdocname: EventAction.call_doctree_resolved(
                    kb, sphinx_app, doctree, fromdocname)
                )

    app.connect(SphinxEvent.EU.value,
                # pragma nocover
                lambda sphinx_app, sphinx_env: EventAction.call_env_updated(
                    kb, sphinx_app, sphinx_env)
                )

    app.connect(SphinxEvent.HCP.value,
                # pragma nocover
                lambda sphinx_app: EventAction.call_html_collect_pages(
                    kb, sphinx_app)
                )

    app.connect(SphinxEvent.ECC.value,
                # pragma nocover
                lambda sphinx_builder,
                       sphinx_env: EventAction.call_env_check_consistency(
                    kb, sphinx_builder, sphinx_env)
                )

    app.connect(SphinxEvent.MR.value,
                # pragma nocover
                lambda sphinx_app, sphinx_env, node,
                       contnode: EventAction.call_missing_reference(
                    kb, sphinx_app, sphinx_env, node, contnode)
                )

    app.connect(SphinxEvent.HPC.value,
                # pragma nocover
                lambda sphinx_app, pagename, templatename, context,
                       doctree: EventAction.call_html_page_context(
                    kb, sphinx_app, pagename, templatename, context, doctree)
                )

    return dict(
        version=__version__,
        parallel_read_safe=False
    )
