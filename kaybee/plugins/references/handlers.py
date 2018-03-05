from typing import List, Dict

from docutils import nodes
from docutils.readers import doctree
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent
from kaybee.plugins.references.container import ReferencesContainer


@kb.event(SphinxEvent.EBRD, scope='references', system_order=40)
def initialize_references_container(kb_app: kb,
                                    sphinx_app: Sphinx,
                                    sphinx_env: BuildEnvironment,
                                    docnames=List[str],
                                    ):
    if not hasattr(sphinx_app.env, 'references'):
        sphinx_app.env.references = ReferencesContainer()


@kb.event(SphinxEvent.EBRD, scope='references', system_order=50)
def register_references(kb_app: kb,
                        sphinx_app: Sphinx,
                        sphinx_env: BuildEnvironment,
                        docnames: List[str]):
    """ Walk the registry and add sphinx directives """

    references: ReferencesContainer = sphinx_app.env.references

    for name, klass in kb_app.config.resources.items():
        # Name is the value in the decorator and directive, e.g.
        # @kb.resource('category') means name=category
        if getattr(klass, 'is_reference', False):
            references[name] = dict()


@kb.event(SphinxEvent.ECC, scope='references', system_order=50)
def add_document_reference(kb_app: kb,
                           sphinx_builder: StandaloneHTMLBuilder,
                           sphinx_env: BuildEnvironment):
    # Moved from the resource directive .run(), this looks at each
    # resource.is_reference. If so, get the reference resource's label
    # and register it in sphinx_app.env.references
    sphinx_app: Sphinx = sphinx_env.app
    resources = sphinx_app.env.resources
    references = sphinx_app.env.references
    for resource in resources.values():
        if getattr(resource, 'is_reference', False):
            label = resource.props.label
            references.add_reference(resource.rtype, label, resource)


@kb.event(SphinxEvent.ECC, scope='references', system_order=60)
def validate_references(kb_app: kb,
                        sphinx_builder: StandaloneHTMLBuilder,
                        sphinx_env: BuildEnvironment):
    # Check the values in props to see if a resource has a reference
    # prop pointing at an invalid reference type, or an invalid reference
    # value. E.g.
    # category: cat1, cat2
    # ...where either 'category' isn't registered as a reference type or
    # 'cat1' isn't registered as a reference value for 'category'.
    resources = sphinx_env.resources
    references = sphinx_env.references

    for resource in resources.values():
        for (reference_label,
             reference_targets) in resource.props.references.items():
            # Make sure this label exists in site.reference
            try:
                site_reference = references[reference_label]
            except KeyError:
                msg = f'''\
            Document {resource.docname} uses unregistered reference label "{
            reference_label}"'''
                raise KeyError(msg)

            # Look through the values on this resource's
            # references['reference'] and ensure they are registered as a
            # target.
            for reference_target in reference_targets:
                try:
                    # Make sure references['reference'] has 'reference1'
                    assert reference_target in site_reference
                except AssertionError:
                    msg = f'''\
            Document {resource.docname} has "{reference_label}" with orphan {
        reference_target} '''
                    raise KeyError(msg)


@kb.event(SphinxEvent.MR, scope='references')
def missing_reference(kb_app: kb,
                      sphinx_app: Sphinx,
                      sphinx_env: BuildEnvironment,
                      node,
                      contnode):
    # The RST might have ref:somescheme values. Sphinx punts to a
    # callback such as this, which picks apart the scheme and expands it.
    references = sphinx_app.env.references
    refdoc = node['refdoc']
    try:
        target_rtype, target_label = node['reftarget'].split('-')
    except ValueError:
        # The scheme might be "python" or "sphinx" or something without
        # a dash. If so, just bail out here.
        return
    target = references.get_reference(target_rtype, target_label)

    if target:
        # Looks like this reference is using one of the Kaybee registered
        # reference types.
        if node['refexplicit']:
            # The ref has a title e.g. :ref:`Some Title <category-python>`
            dispname = contnode.children[0]
        else:
            # Use the title from the target
            dispname = target.title

        uri = sphinx_app.builder.get_relative_uri(refdoc, target.docname)
        newnode = nodes.reference('', '', internal=True, refuri=uri,
                                  reftitle=dispname)
        emp = nodes.emphasis()
        newnode.append(emp)
        emp.append(nodes.Text(dispname))
        return newnode


@kb.event(SphinxEvent.HPC, scope='references')
def references_into_html_context(
        kb_app: kb,
        sphinx_app: Sphinx,
        pagename,
        templatename: str,
        context,
        doctree: doctree) -> Dict[str, str]:
    # Always put the references db into Jinja2 context
    context['references'] = sphinx_app.env.references


@kb.dumper('references')
def dump_settings(kb_app: kb, sphinx_env: BuildEnvironment):
    # First get the kb app configuration for references
    config = {
        k: v.__module__ + '.' + v.__name__
        for (k, v) in kb_app.config.resources.items()
        if getattr(v, 'is_reference', False)
    }

    # Next, get the actual references in the app.references DB
    references = sphinx_env.references
    resources = sphinx_env.resources
    values = dict()
    for k, v in references.items():
        values[k] = dict()
        for label, resource in v.items():
            values[k][label] = resource.__json__(resources)

    references = dict(
        config=config,
        values=values
    )
    return dict(references=references)
