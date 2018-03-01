from typing import List

from docutils.parsers.rst import Directive

from kaybee import app
from kaybee.plugins.widgets.node import widget


class WidgetDirective(Directive):
    has_content = True

    @classmethod
    def get_widget_class(cls, widget_directive):
        """ Make this easy to mock """
        return app.kb.config.widgets[widget_directive]

    @classmethod
    def split_content(cls, content: List[str]):
        # The directive gives us the RST body in this directive as
        # a list of strings, one for each line, with empty strings for
        # blank lines. Start by re-assembling one big string (would be
        # better to do some iterator-thingy.)
        content = '\n'.join(content)

        # First strip any leading/trailing blank lines from indented content
        content = content.strip()

        # Split the YAML from the rest of the body, if any blank
        # lines in the middle
        split_content = content.split('\n\n')
        yaml_content = split_content[0]

        # Re-assemble the RST content in the widget body, if any
        if len(split_content) > 1:
            rst_content = '\n\n'.join(split_content[1:])
        else:
            rst_content = None

        return yaml_content, rst_content

    def get_widget(self, docname):
        # Get the info from this directive and make instance
        wtype = self.name

        yaml_content, rst_content = self.split_content(self.content)
        widget_content = '\n'.join(self.content)
        widget_class = WidgetDirective.get_widget_class(wtype)
        return widget_class(docname, wtype, yaml_content, rst_content)

    @property
    def docname(self):
        return self.state.document.settings.env.docname

    @property
    def widgets(self):
        return self.state.document.settings.env.widgets

    def run(self):
        """ Run at parse time.

        When the documents are initially being scanned, this method runs
        and does two things: (a) creates an instance that is added to
        the site's widgets, and (b) leaves behind a placeholder docutils
        node that can later be processed after the docs are resolved.
        The latter needs enough information to retrieve the former.

        """

        this_widget = self.get_widget(self.docname)

        self.widgets[repr(this_widget)] = this_widget

        # Now add the node to the doctree
        widget_node = widget()
        ids = [repr(this_widget)]
        names = [self.name]
        attrs = dict(ids=ids, names=names)
        widget_node.update_basic_atts(attrs)
        return [widget_node]
