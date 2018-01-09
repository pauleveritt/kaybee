from docutils.parsers.rst import Directive


class BaseWidgetDirective(Directive):
    has_content = True
