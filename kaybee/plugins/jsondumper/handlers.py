import datetime
import json

import os
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent
from kaybee.plugins.jsondumper.action import JsondumperAction


def datetime_handler(x):
    """ Allow serializing datetime objects to JSON """
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


@kb.event(SphinxEvent.ECC, scope='jsondump', system_order=80)
def generate_json_info(kb_app: kb, builder: StandaloneHTMLBuilder,
                        sphinx_env: BuildEnvironment):

    # Get all the jsondumpers and dump their results
    jsondumpers = JsondumperAction.get_callbacks(kb_app)
    jsondumper_results = [jsondumper(kb_app, sphinx_env) for jsondumper in jsondumpers]
    output = {k: v for d in jsondumper_results for k, v in d.items()}

    # Now write the result to disk
    filename = output['filename']
    results = output['results']
    output_filename = os.path.join(builder.outdir, filename)
    with open(output_filename, 'w') as f:
        json.dump(results, f, default=datetime_handler)
