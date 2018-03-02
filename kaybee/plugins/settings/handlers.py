from sphinx.environment import BuildEnvironment

from kaybee.app import kb


@kb.dumper('settings')
def dump_settings(kb_app: kb, sphinx_env: BuildEnvironment):
    settings = sphinx_env.config.kaybee_settings.dict()
    return dict(settings=settings)
