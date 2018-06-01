import json
import os

from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent
from kaybee.plugins.jsondumper.action import JsondumperAction
from kaybee.utils.datetime_handler import datetime_handler


@kb.event(SphinxEvent.ECC, scope='jsondump', system_order=80)
def generate_json_info(kb_app: kb, builder: StandaloneHTMLBuilder,
                       sphinx_env: BuildEnvironment):
    # Get all the jsondumpers and dump their results
    jsondumpers = JsondumperAction.get_callbacks(kb_app)
    for jsondumper in jsondumpers:
        jsondumper_results = jsondumper(kb_app, sphinx_env)
        filename = jsondumper_results['filename']
        results = jsondumper_results['results']
        output_filename = os.path.join(builder.outdir, filename)
        with open(output_filename, 'w') as f:
            json.dump(results, f, default=datetime_handler)

    # For fun, let's dump all the resources (without the body) and the
    # references, as is
    resources = {}
    for resource in sphinx_env.resources.values():
        resources[resource.docname] = resource.__json__(sphinx_env.resources)

    #
    new_results = dict(
        resources=resources
    )
    new_output_filename = os.path.join(builder.outdir, 'catalog.json')
    with open(new_output_filename, 'w') as f:
        json.dump(new_results, f, default=datetime_handler)
