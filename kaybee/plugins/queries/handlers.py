from typing import List

from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent


@kb.event(SphinxEvent.EBRD, scope='queries', system_order=40)
def initialize_query_service(kb_app: kb,
                             sphinx_app: Sphinx,
                             sphinx_env: BuildEnvironment,
                             docnames=List[str],
                             ):
    sphinx_app.query = dict()

#
# @kb.event(SphinxEvent.DREAD, scope='genericpage')
# def add_genericpage(kb_app: kb, sphinx_app: Sphinx,
#                     doctree: doctree):
#     resources = sphinx_app.resources
#
#     confdir = sphinx_app.confdir
#     source = PurePath(doctree.attributes['source'])
#
#     # Get the relative path inside the docs dir, without .rst, then
#     # get the resource
#     docname = str(source.relative_to(confdir)).split('.rst')[0]
#
#     resource = resources.get(docname)
#     if resource is None:
#         # Couldn't find a resource for this document, so let's make it
#         # a genericpage
#         gp_class = GenericpageAction.get_genericpage(kb_app)
#         gp = gp_class(docname)
#         sphinx_app.genericpages[docname] = gp
#         return gp
#
#
# @kb.event(SphinxEvent.HPC, scope='genericpage')
# def genericpage_into_html_context(
#         kb_app: kb,
#         sphinx_app: Sphinx,
#         pagename,
#         templatename: str,
#         context,
#         doctree: doctree) -> Dict[str, str]:
#     # Get the resource for this pagename. If no match, then this pagename
#     # must be a genericpage
#     resources = sphinx_app.resources
#     resource = resources.get(pagename)
#     if not resource:
#         genericpages = sphinx_app.genericpages
#         gp = genericpages.get(pagename)
#         if gp:
#             context['genericpage'] = gp
#             template = gp.template(resources)
#             templatename = template + '.html'
#             return dict(templatename=templatename)

#
# @kb.dumper('queries')
# def dump_settings(kb_app: kb, sphinx_env: BuildEnvironment):
#     config = {
#         k: v.__module__ + '.' + v.__name__
#         for (k, v) in kb_app.config.genericpages.items()
#     }
#
#     # Get the Genericpage values in the app
#     values = {}
#     resources = sphinx_env.app.resources
#     gps = sphinx_env.app.genericpages
#     values = {k: v.__json__(resources) for (k, v) in gps.items()}
#
#     genericpages = dict(
#         config=config,
#         values=values
#     )
#     return dict(genericpages=genericpages)
