"""

Built-in registry app that can be used directly in docs projects.

The app defines a set of configured actions. These come mostly from
plugins. Kaybee ships with some built-in plugins, and this app bundles
them up.

Other sites might have other plugins and thus need a custom subclass for
the app.

"""
import dectate

from kaybee.plugins.events import EventAction


class kb(dectate.App):
    event = dectate.directive(EventAction)
