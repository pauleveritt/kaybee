from docutils.readers import doctree
from sphinx.application import Sphinx

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent


@kb.event(SphinxEvent.HPC, scope='sphinx_app')
def sphinx_app_html_context(
        kb_app: kb,
        sphinx_app: Sphinx,
        pagename,
        templatename: str,
        context,
        doctree: doctree,
):
    context['sphinx_app'] = sphinx_app
    context['kaybee_settings'] = sphinx_app.config.kaybee_settings
