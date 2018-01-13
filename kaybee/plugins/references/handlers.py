from typing import List

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent
from kaybee.plugins.references.container import ReferencesContainer
from kaybee.plugins.references.model_types import ReferencesType


def reference_fieldnames(resource):
    """ Look in model and return each fieldname that is a reference """

    return [
        field.name
        for field in resource.props.fields.values()
        if field.type_ == ReferencesType
    ]


def get_reference_classes(resource_classes):
    """ Given resource classes from config, filter is_reference """

    return [rc for rc in resource_classes
            if getattr(rc, 'is_reference', False)]


@kb.event(SphinxEvent.EBRD, scope='references', system_order=40)
def initialize_references_container(kb_app: kb,
                                    sphinx_app: Sphinx,
                                    sphinx_env: BuildEnvironment,
                                    docnames=List[str],
                                    ):
    sphinx_app.references = ReferencesContainer()


@kb.event(SphinxEvent.EBRD, scope='references', system_order=50)
def register_references(kb_app: kb,
                        sphinx_app: Sphinx,
                        sphinx_env: BuildEnvironment,
                        docnames: List[str]):
    """ Walk the registry and add sphinx directives """

    references: ReferencesContainer = sphinx_app.references

    for name, klass in kb_app.config.resources.items():
        # Name is the value in the decorator and directive, e.g.
        # @kb.reference('category') means name=category
        if getattr(klass, 'is_reference', False):
            references[name] = dict()


@kb.event(SphinxEvent.ECC, scope='references')
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
        for field_name in reference_fieldnames(resource):
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


@kb.event(SphinxEvent.MR, scope='references')
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


@kb.dumper('references')
def dump_settings(kb_app: kb, sphinx_env: BuildEnvironment):
    # First get the kb app configuration for references
    config = {
        k: v.__module__ + '.' + v.__name__
        for (k, v) in kb_app.config.resources.items()
        if getattr(v, 'is_reference', False)
    }

    # Next, get the actual references in the app.references DB
    references = sphinx_env.app.references
    resources = sphinx_env.app.resources
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
