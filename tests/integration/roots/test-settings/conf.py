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


@kb.dumper('demosettings')
def dump_hello(kb_app: kb, sphinx_env: BuildEnvironment):
    settings = sphinx_env.app.config['kaybee_settings']
    use_debug = settings.debugdumper.use_debug
    return dict(
        demosettings=dict(using_demo=use_debug)
    )
