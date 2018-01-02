import datetime
from sphinx.environment import BuildEnvironment

from kaybee.app import kb


@kb.dumper('testdumper')
def dump_hello(kb_app: kb, sphinx_env: BuildEnvironment):
    then = datetime.datetime(2017, 12, 30, 12, 00, 00)
    return dict(then=then)
