import datetime
import json

import dectate
import os
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.environment import BuildEnvironment

from kaybee.app import kb
from kaybee.plugins.events import SphinxEvent


def datetime_handler(x):
    """ Allow serializing datetime objects to JSON """
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


class DumperAction(dectate.Action):
    config = {
        'dumpers': dict
    }

    def __init__(self, name: str):
        super().__init__()
        self.name = name

    def identifier(self, dumpers):
        return self.name

    # noinspection PyMethodOverriding
    def perform(self, obj, dumpers):
        dumpers[self.name] = obj

    @classmethod
    def get_callbacks(cls, registry):
        # Presumes the registry has been committed

        q = dectate.Query('dumper')
        return [args[1] for args in q(registry)]


@kb.event(SphinxEvent.ECC, 'debugdump')
def generate_debug_info(kb_app: kb, builder: StandaloneHTMLBuilder,
                        sphinx_env: BuildEnvironment):

    # Get all the dumpers and dump their results
    dumpers = DumperAction.get_callbacks(kb_app)
    dumper_results = [dumper(kb_app) for dumper in dumpers]
    result = {k: v for d in dumper_results for k, v in d.items()}

    # Now write the result to disk
    output_filename = os.path.join(builder.outdir, 'debug_dump.json')
    with open(output_filename, 'w') as f:
        json.dump(result, f, default=datetime_handler)
