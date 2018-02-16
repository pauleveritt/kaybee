"""

Built-in registry app that can be used directly in docs projects.

The app defines a set of configured actions. These come mostly from
plugins. Kaybee ships with some built-in plugins, and this app bundles
them up.

Other sites might have other plugins and thus need a custom subclass for
the app.

"""
import dectate

from kaybee.plugins.articles.actions import ToctreeAction
from kaybee.plugins.debugdumper.action import DumperAction
from kaybee.plugins.events import EventAction
from kaybee.plugins.genericpage.action import GenericpageAction
from kaybee.plugins.postrenderer.action import PostrendererAction
from kaybee.plugins.resources.action import ResourceAction
from kaybee.plugins.widgets.action import WidgetAction


class kb(dectate.App):
    event = dectate.directive(EventAction)
    dumper = dectate.directive(DumperAction)
    resource = dectate.directive(ResourceAction)
    genericpage = dectate.directive(GenericpageAction)
    widget = dectate.directive(WidgetAction)
    toctree = dectate.directive(ToctreeAction)
    postrenderer = dectate.directive(PostrendererAction)
