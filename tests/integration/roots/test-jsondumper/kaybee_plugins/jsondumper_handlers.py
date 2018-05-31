from sphinx.environment import BuildEnvironment

from kaybee.app import kb


@kb.jsondumper('testjsondumper')
def dump_some_resources(kb_app: kb, sphinx_env: BuildEnvironment):
    return dict(
        filename='testjsondumper.json',
        results=[
            dict(
                docname='a/b/1',
                title='One'
            ),
            dict(
                docname='a/b/2',
                title='Two'
            )
        ]
    )
