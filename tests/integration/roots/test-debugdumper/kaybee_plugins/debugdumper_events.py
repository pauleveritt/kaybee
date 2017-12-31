from sphinx.environment import BuildEnvironment

from kaybee.app import kb


@kb.dumper('testdumper')
def dump_hello(kb_app: kb, sphinx_env: BuildEnvironment):
    return dict(hello='world')
