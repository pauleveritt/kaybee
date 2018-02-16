"""
Sphinx Template Bridge

Sphinx renders the HTML "body". We'd like to customize that without
writing a complete builder. Instead, we'll override the TemplateBridge
and take the HTML rendered output, then customize it before returning.

We'll do that by allowing the registration of "processors", for example
an XSLT transform.
"""

from sphinx.jinja2glue import BuiltinTemplateLoader

from kaybee.app import kb
from kaybee.plugins.postrenderer.action import PostrendererAction


class KaybeeBridge(BuiltinTemplateLoader):

    def get_kb(self):
        # Make it easy to mock this in text
        return kb

    def render(self, template, context):
        output = super().render(template, context)

        kb_app = self.get_kb()
        postrenderers = PostrendererAction.get_callbacks(kb_app)
        for postrenderer in postrenderers:
            pr = postrenderer()
            output = pr(output, context)

        return output
