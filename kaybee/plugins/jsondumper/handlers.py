import datetime
import json

import os
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent
from kaybee.plugins.jsondumper.action import DumperAction


def datetime_handler(x):
    """ Allow serializing datetime objects to JSON """
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


@kb.event(SphinxEvent.ECC, scope='jsondump', system_order=80)
def generate_json_info(kb_app: kb, builder: StandaloneHTMLBuilder,
                        sphinx_env: BuildEnvironment):
    # If the config value doesn't enable dumping, bail out
    dumper_settings = sphinx_env.app.config.kaybee_settings.jsondumper
    use_jsondump = dumper_settings.use_jsondump

    if not use_jsondump:
        return

    # Get all the dumpers and dump their results
    dumpers = DumperAction.get_callbacks(kb_app)
    dumper_results = [dumper(kb_app, sphinx_env) for dumper in dumpers]
    result = {k: v for d in dumper_results for k, v in d.items()}

    # Now write the result to disk
    output_filename = os.path.join(builder.outdir, 'json_dump.json')
    with open(output_filename, 'w') as f:
        json.dump(result, f, default=datetime_handler)
