"""

Jinja2 filters

The articles system needs some rich ways to format things. For
example, different ways to show dates. We'll use Jinja2 filters for
this.

The filters are registered as instance callables. This lets us put
psuedo-globals such as sphinx_app into the scope and not have to
pass that in from the template usage.

"""

from sphinx.application import Sphinx


class BaseFilter:
    def __init__(self, sphinx_app: Sphinx):
        self.sphinx_app = sphinx_app


class DatetimeFilter(BaseFilter):
    def __call__(self, date_value, fmt='long'):
        if date_value is None:
            # Some resource props values are None
            return

        # Get the setting from the articles setting
        settings = self.sphinx_app.config.kaybee_settings.articles
        fmt_setting = getattr(settings, 'datefmt_' + fmt)

        # Return value
        response = date_value.strftime(fmt_setting)
        return response
