import importscan
from sphinx.application import Sphinx

from kaybee import plugins
from kaybee.app import kb
from kaybee.plugins.events import EventAction, SphinxEvent

__version__ = '0.0.7'
__title__ = "kaybee"


def setup(app: Sphinx):
    """ Initialize Kaybee as a Sphinx extension """

    importscan.scan(plugins)

    app.connect(SphinxEvent.BI.value,
                lambda sphinx_app: EventAction.call_builder_init(
                    kb, sphinx_app)
                )
    app.connect(SphinxEvent.EPD.value,
                lambda sphinx_app, sphinx_env,
                       docname: EventAction.call_purge_doc(
                    kb, sphinx_app, sphinx_env, docname)
                )

    app.connect(SphinxEvent.EBRD.value,
                lambda sphinx_app, sphinx_env,
                       docnames: EventAction.call_env_before_read_docs(
                    kb, sphinx_app, sphinx_env, docnames)
                )

    app.connect(SphinxEvent.DRES.value,
                lambda sphinx_app, doctree,
                       fromdocname: EventAction.call_doctree_resolved(
                    kb, sphinx_app, doctree, fromdocname)
                )

    app.connect(SphinxEvent.HCP.value,
                lambda sphinx_app: EventAction.call_html_collect_pages(
                    kb, sphinx_app)
                )

    app.connect(SphinxEvent.ECC.value,
                lambda sphinx_builder,
                       sphinx_env: EventAction.call_env_check_consistency(
                    kb, sphinx_builder, sphinx_env)
                )

    app.connect(SphinxEvent.MR.value,
                lambda sphinx_app, sphinx_env, node,
                       contnode: EventAction.call_missing_reference(
                    kb, sphinx_app, sphinx_env, node, contnode)
                )

    app.connect(SphinxEvent.HPC.value,
                lambda sphinx_app, pagename, templatename, context,
                       doctree: EventAction.call_html_page_context(
                    kb, sphinx_app, pagename, templatename, context, doctree)
                )

    return dict(
        version=__version__,
        parallel_read_safe=False
    )
