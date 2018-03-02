from typing import Mapping

from pydantic import BaseModel
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util.osutil import relative_uri

from kaybee.utils.models import load_model
from kaybee.utils.rst import rst_to_html


class BaseWidgetModel(BaseModel):
    name: str  # Must be unique on each page
    template: str = None  # Can come from class name

    class Config:
        ignore_extra = False


class BaseWidget:
    docname: str  # Widget instances get registered from a doc
    wtype: str  # This is the directive name, e.g. listing
    props: BaseWidgetModel
    rst_content: str  # The body rst converted to HTML

    def __init__(self, docname: str, wtype: str,
                 yaml_content: str,
                 rst_content: str = None):
        self.docname = docname
        self.wtype = wtype
        model = self.__annotations__['props']
        self.props: BaseWidgetModel = load_model(docname, model, yaml_content)

        if rst_content:
            self.content = rst_to_html(rst_content)

    def __repr__(self):
        return f'{self.docname}-{self.props.name}'

    def pathto_docname(self, target_docname):
        """ Mimic the sphinx.builders.html.pathto inline closure.

        We need a way to resolve relative URLs so hrefs work when a Sphinx
        site is served in a subdirectory. Sphinx has an odd inline function
        called pathto that has some local variables. This function serves the
        purpose for paths to docs as well as static resourcees. Let's split
        that and have our own, for widgets which aren't using the Sphinx
        Jinja2 renderer.

        """

        uri = relative_uri(self.docname, target_docname)
        return uri

    @property
    def template(self):
        """ Get the template from: YAML or class """

        # First try props
        if self.props.template:
            return self.props.template
        else:
            # Return the wtype of the widget, and we'll presume that,
            # like resources, there's a .html file in that directory
            return self.wtype

    def make_context(self, context: Mapping, sphinx_app: Sphinx):
        pass

    def render(self, sphinx_app: Sphinx, context):
        """ Given a Sphinx builder and context with sphinx_app in it,
         generate HTML """

        # Called from kaybee.plugins.widgets.handlers.render_widgets

        builder: StandaloneHTMLBuilder = sphinx_app.builder
        resource = sphinx_app.env.resources[self.docname]
        context['sphinx_app'] = sphinx_app
        context['widget'] = self
        context['resource'] = resource

        # make_context is optionally implemented on the concrete class
        # for each widget
        self.make_context(context, sphinx_app)

        # NOTE: Can use builder.templates.render_string
        template = self.template + '.html'
        html = builder.templates.render(template, context)
        return html

    def __json__(self):
        # The root has different rules about parents
        return dict(
            docname=self.docname,
            template=self.props.template,
            wtype=self.wtype,
            props=self.props.dict(),
            repr=repr(self),
        )
