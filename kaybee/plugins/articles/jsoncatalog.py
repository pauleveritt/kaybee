"""

Dump the resources and references to a standard JSON format/file
at a predictable location.

"""
import json
import os

from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent
from kaybee.utils.datetime_handler import datetime_handler


def clean_resource_json(resource_json):
    """ The catalog wants to be smaller, let's drop some stuff """

    for a in ('parent_docname', 'parent', 'template', 'repr', 'series'):
        if a in resource_json:
            del resource_json[a]

    props = resource_json['props']
    for prop in (
            'acquireds', 'style', 'in_nav', 'nav_title', 'weight',
            'auto_excerpt'):
        if prop in props:
            del props[prop]

    return resource_json


def resources_to_json(resources):
    """ Make a JSON/catalog representation of the resources db """
    return {
        docname: clean_resource_json(resource.__json__(resources))
        for (docname, resource)
        in resources.items()
    }


def references_to_json(resources, references):
    """ Make a JSON/catalog representation of the references db,
     including the count for each """

    dump_references = {}
    for reftype, refvalue in references.items():
        dump_references[reftype] = {}
        for label, reference_resource in refvalue.items():
            target_count = len(reference_resource.get_sources(resources))
            dump_references[reftype][label] = dict(
                count=target_count,
                docname=reference_resource.docname
            )

    return dump_references


@kb.event(SphinxEvent.ECC, scope='jsoncatalog', system_order=80)
def generate_json_catalog(kb_app: kb, builder: StandaloneHTMLBuilder,
                          sphinx_env: BuildEnvironment):
    # Collect the information to dump
    resources = resources_to_json(sphinx_env.resources)
    references = references_to_json(sphinx_env.resources,
                                    sphinx_env.references)
    output = dict(resources=resources, references=references)

    # Write to a file
    output_filename = os.path.join(builder.outdir, 'catalog.json')
    with open(output_filename, 'w') as f:
        json.dump(output, f, default=datetime_handler)
