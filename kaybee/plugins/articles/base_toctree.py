'''

Intercept and re-render Sphinx built-in toctrees.

This class renders alternate HTML for the existing Sphinx toctree.
You use toctree as normal, then during Sphinx processing events, we find
toctrees and re-render them with our HTML.

Why not make our own directive? toctrees are complex. Working with the
rendering of the existing version is easier.

'''

from typing import List, Tuple


class BaseToctree:
    """ Basis for a subclass with a model and template """
    entries: List = []
    result_count = 0
    template = 'toctree'

    def set_entries(self, entries: List[Tuple[str, str]], titles, resources):
        """ Provide the template the data for the toc entries """
        self.entries = []
        for flag, pagename in entries:
            title = titles[pagename].children[0]
            resource = resources.get(pagename, None)
            if resource and not resource.is_published():
                continue
            self.entries.append(dict(
                title=title, href=pagename, resource=resource
            ))

        self.result_count = len(self.entries)

    def render(self, builder, context, site):
        """ Given a Sphinx builder and context with site in it,
         generate HTML """

        context['site'] = site
        context['widget'] = self

        html = builder.templates.render(self.template(), context)
        return html
