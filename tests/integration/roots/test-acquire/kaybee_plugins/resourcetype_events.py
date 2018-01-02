from sphinx.environment import BuildEnvironment

from kaybee.app import kb


@kb.dumper('resourcedumper')
def resourcedumper(kb_app: kb, sphinx_env: BuildEnvironment):
    # Let's increase test coverage during integration testing by dumping
    # a few resource things:
    # - docnames of parents
    # - repr of a doc
    testing = dict()
    resources = sphinx_env.app.resources
    for resource in resources.values():
        if resource.docname == 'index':
            # Special rule for the root
            testing[resource.docname] = dict(
                parent_docnames=resource.parents(resources),
                repr=repr(resource)
            )
        else:
            testing[resource.docname] = dict(
                parent_docnames=[p.docname for p in
                                 resource.parents(resources)],
                repr=repr(resource)
            )
    return dict(testing=testing)
