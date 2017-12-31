from sphinx.environment import BuildEnvironment

import kaybee
from kaybee.app import kb

extensions = [kaybee.__title__]

master_doc = 'index'
html_title = ''
exclude_patterns = ['_build']

kaybee_settings = kaybee.KaybeeSettings(
    debugdumper=dict(
        use_debug=True
    )
)


@kb.dumper('testdumper')
def dump_hello(kb_app: kb, sphinx_env: BuildEnvironment):
    return dict(hello='world')
