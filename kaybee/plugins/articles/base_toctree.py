"""

Intercept and re-render Sphinx built-in toctrees.

This class renders alternate HTML for the existing Sphinx toctree.
You use toctree as normal, then during Sphinx processing events, we find
toctrees and re-render them with our HTML.

Why not make our own directive? toctrees are complex. Working with the
rendering of the existing version is easier.

"""

from typing import List, Tuple

from sphinx.application import Sphinx
from sphinx.util.osutil import relative_uri


class BaseToctree:
    """ Basis for a subclass with a template """
    entries: List = []
    result_count = 0
    template = 'toctree'

    def __init__(self, docname: str):
        self.docname = docname

    def set_entries(self, entries: List[Tuple[str, str]], titles, resources):
        """ Provide the template the data for the toc entries """

        self.entries = []
        for flag, pagename in entries:
            title = titles[pagename].children[0]
            resource = resources.get(pagename, None)
            if resource and hasattr(resource,
                                    'is_published') and not \
                    resource.is_published:
                continue
            # Even if there is no resource for this tocentry, we can
            # use the toctree info
            self.entries.append(dict(
                title=title, href=pagename, resource=resource
            ))

        self.result_count = len(self.entries)

    def pathto_docname(self, target_docname):
        """ Mimic the sphinx.builders.html.pathto inline closure.

        We need a way to resolve relative URLs so hrefs work when a Sphinx
        site is served in a subdirectory. Sphinx has an odd inline function
        called pathto that has some local variables. This function serves the
        purpose for paths to docs as well as static resourcees. Let's split
        that and have our own, for widgets which aren't using the Sphinx
        Jinja2 renderer.

        """

        uri = relative_uri(self.docname, target_docname)
        return uri

    def render(self, builder, context, sphinx_app: Sphinx):
        """ Given a Sphinx builder and context with site in it,
         generate HTML """

        context['sphinx_app'] = sphinx_app
        context['toctree'] = self

        html = builder.templates.render(self.template + '.html', context)
        return html
