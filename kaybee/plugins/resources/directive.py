from docutils.parsers.rst import Directive

from kaybee import app


class ResourceDirective(Directive):
    has_content = True

    @classmethod
    def get_resource_class(cls, resource_directive):
        """ Make this easy to mock """
        return app.kb.config.resources[resource_directive]

    @property
    def docname(self):
        return self.state.document.settings.env.docname

    @property
    def resources(self):
        return self.state.document.settings.env.resources

    def run(self):
        """ Run at parse time.

        When the documents are initially being scanned, this method runs
        and does two things: (a) creates an instance that is added to
        the site's widgets, and (b) leaves behind a placeholder docutils
        node that can later be processed after the docs are resolved.
        The latter needs enough information to retrieve the former.

        """

        rtype = self.name
        resource_content = '\n'.join(self.content)
        resource_class = ResourceDirective.get_resource_class(rtype)
        this_resource = resource_class(self.docname, rtype, resource_content)

        # Add this resource to the site
        self.resources[this_resource.docname] = this_resource

        # Don't need to return a resource "node", the document is the node
        return []
