from sphinx.environment import BuildEnvironment

from kaybee.app import kb


@kb.dumper('demosettings')
def dump_hello(kb_app: kb, sphinx_env: BuildEnvironment):
    settings = sphinx_env.app.config['kaybee_settings']
    use_debug = settings.debugdumper.use_debug
    return dict(
        demosettings=dict(using_demo=use_debug)
    )
