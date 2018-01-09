from sphinx.environment import BuildEnvironment

from kaybee.app import kb


@kb.dumper('widgets')
def dump_settings(kb_app: kb, sphinx_env: BuildEnvironment):
    # First get the kb app configuration for widgets
    config = {
        k: v.__module__ + '.' + v.__name__
        for (k, v) in kb_app.config.widgets.items()
    }

    widgets = dict(
        config=config,
    )
    return dict(widgets=widgets)
