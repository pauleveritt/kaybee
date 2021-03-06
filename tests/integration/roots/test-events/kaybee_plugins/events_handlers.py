from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent


@kb.event(SphinxEvent.BI)
def handle_builderinit(kb_app: kb, sphinx_app):
    sphinx_app.bi = 'BI'


@kb.event(SphinxEvent.EPD)
def handle_purgedoc(kb_app, sphinx_app, sphinx_env, docname):
    sphinx_app.epd = 'EPD'


@kb.event(SphinxEvent.EBRD)
def handle_before_read_docs(kb_app, sphinx_app, sphinx_env,
                            docnames):
    sphinx_app.ebrd = 'EBRD'


@kb.event(SphinxEvent.DREAD)
def handle_doctree_read(kb_app, sphinx_app, sphinx_doctree):
    sphinx_app.dread = 'DREAD'


@kb.event(SphinxEvent.DRES)
def handle_doctree_resolved(kb_app, sphinx_app, sphinx_doctree,
                            fromdocname):
    sphinx_app.dres = 'DRES'


@kb.event(SphinxEvent.MR)
def handle_missing_reference(kb_app, sphinx_app,
                             sphinx_env, node, contnode):
    sphinx_app.mr = 'MR'


@kb.event(SphinxEvent.ECC)
def handle_check_consistency(kb_app, html_builder, sphinx_env):
    kb_app.ecc = 'ECC'


@kb.event(SphinxEvent.HCP)
def handle_collect_pages(kb_app, sphinx_app):
    sphinx_app.hcp = 'hcp'
    return iter(['', '', 'page.html'])


@kb.event(SphinxEvent.HPC)
def add_context(kb_app: kb, sphinx_app, pagename, templatename,
                context, doctree):
    sphinx_app.hpc = 'HPC'
    context['sphinx_app'] = sphinx_app
    context['kb_app'] = kb_app
