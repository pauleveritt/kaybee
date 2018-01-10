from typing import Mapping

from pydantic import BaseModel
from sphinx.application import Sphinx
from sphinx.builders.html import StandaloneHTMLBuilder

from kaybee.utils.models import load_model


class BaseWidgetModel(BaseModel):
    name: str  # Must be unique on each page
    template: str


class BaseWidget:
    docname: str  # Widget instances get registered from a doc
    wtype: str  # This is the directive name, e.g. listing
    model = BaseWidgetModel

    def __init__(self, docname: str, wtype: str, yaml_content: str):
        self.docname = docname
        self.wtype = wtype
        self.props: BaseWidgetModel = load_model(self.model, yaml_content)

    def __repr__(self):
        return f'{self.docname}-{self.props.name}'

    def make_context(self, context: Mapping, sphinx_app: Sphinx):
        raise NotImplementedError

    def render(self, sphinx_app: Sphinx, context):
        """ Given a Sphinx builder and context with sphinx_app in it,
         generate HTML """

        builder: StandaloneHTMLBuilder = sphinx_app.builder
        resource = sphinx_app.resources[self.docname]
        context['sphinx_app'] = sphinx_app
        context['widget'] = self
        context['resource'] = resource

        # make_context is optionally implemented on the concrete class
        # for each widget
        self.make_context(context, sphinx_app)

        # NOTE: Can use builder.templates.render_string
        html = builder.templates.render(self.props.template, context)
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
