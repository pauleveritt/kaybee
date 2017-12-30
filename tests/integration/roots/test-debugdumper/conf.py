import kaybee
from kaybee.app import kb

extensions = [kaybee.__title__]

master_doc = 'index'
html_title = ''
exclude_patterns = ['_build']


@kb.dumper('testdumper')
def dump_hello(kb_app: kb):
    return dict(hello='world')

