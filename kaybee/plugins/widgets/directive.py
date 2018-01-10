from docutils.parsers.rst import Directive

from kaybee import app
from kaybee.plugins.widgets.node import widget


class WidgetDirective(Directive):
    has_content = True

    @classmethod
    def get_widget_class(cls, widget_directive):
        """ Make this easy to mock """
        return app.kb.config.widgets[widget_directive]

    def get_widget(self, docname):
        # Get the info from this directive and make instance
        rtype = self.name
        widget_content = '\n'.join(self.content)
        widget_class = WidgetDirective.get_widget_class(rtype)
        return widget_class(docname, rtype, widget_content)

    @property
    def docname(self):
        return self.state.document.settings.env.docname

    @property
    def widgets(self):
        return self.state.document.settings.env.app.widgets

    def run(self):
        """ Run at parse time.

        When the documents are initially being scanned, this method runs
        and does two things: (a) creates an instance that is added to
        the site's widgets, and (b) leaves behind a placeholder docutils
        node that can later be processed after the docs are resolved.
        The latter needs enough information to retrieve the former.

        """

        this_widget = self.get_widget(self.docname)

        self.widgets[this_widget.docname] = this_widget

        # Now add the node to the doctree
        widget_node = widget()
        attrs = dict(ids=[this_widget.docname], names=[self.name])
        widget_node.update_basic_atts(attrs)
        return [widget_node]
