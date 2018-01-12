from docutils import nodes
from typing import List

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
    sphinx_app.references = ReferencesContainer()


@kb.event(SphinxEvent.EBRD, 'references', system_order=50)
def register_references(kb_app: kb,
                        sphinx_app: Sphinx,
                        sphinx_env: BuildEnvironment,
                        docnames: List[str]):
    """ Walk the registry and add sphinx directives """

    references: ReferencesContainer = sphinx_app.references

    for name, klass in kb_app.config.references.items():
        # Name is the value in the decorator and directive, e.g.
        # @kb.reference('category') means name=category
        if getattr(klass, 'is_reference', False):
            references[name] = dict()


@kb.event(SphinxEvent.ECC, 'references')
def validate_references(kb_app: kb,
                        sphinx_builder: StandaloneHTMLBuilder,
                        sphinx_env: BuildEnvironment):
    # Check the values in props to see if a resource has a reference
    # prop pointing at an invalid reference type, or an invalid reference
    # value. E.g.
    # category: cat1, cat2
    # ...where either 'category' isn't registered as a reference type or
    # 'cat1' isn't registered as a reference value for 'category'.
    resources = sphinx_env.app.resources
    references = sphinx_env.app.references

    for resource in resources.values():
        # This line looks at the props model to see which props are marked
        # as reference-able
        for field_name in resource.reference_fieldnames:
            # And this looks at this resource's props for that field, and
            # each of the values in the sequence.
            for target_label in getattr(resource.props, field_name):
                # Make sure this label exists in site.reference
                try:
                    srfn = references[field_name]
                except KeyError:
                    msg = f'''\
                Document {resource.docname} has unregistered reference "{
                field_name}"'''
                    raise KeyError(msg)
                try:
                    # Make sure references['category'] has 'category1'
                    assert target_label in srfn
                except AssertionError:
                    msg = f'''\
                Document {resource.docname} has "{field_name}" with orphan {
                target_label} '''
                    raise KeyError(msg)


@kb.event(SphinxEvent.MR, 'references')
def missing_reference(kb_app: kb,
                      sphinx_app: Sphinx,
                      sphinx_env: BuildEnvironment,
                      node,
                      contnode):
    # The RST might have ref:somescheme values. Sphinx punts to a
    # callback such as this, which picks apart the scheme and expands it.
    references = sphinx_env.app.references
    refdoc = node['refdoc']
    target_rtype, target_label = node['reftarget'].split('-')
    target = references.get_reference(target_rtype, target_label)

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
