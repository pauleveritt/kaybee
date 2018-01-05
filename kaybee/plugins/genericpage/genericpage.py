class Genericpage:
    def __init__(self, docname):
        self.docname = docname

    def __repr__(self):
        # Primarily useful in pytest parameters
        return self.docname

    @classmethod
    def template(cls, resources):
        # By default, just use the Sphinx built-in template for pages
        templatename = 'page'

        root = resources.get('index', False)
        if root:
            acquireds = getattr(root.props, 'acquireds', False)
            if acquireds:
                # First try in the per-type acquireds
                gp_acquireds = acquireds.get('genericpage')
                if gp_acquireds:
                    prop_acquired = gp_acquireds.get('template')
                    if prop_acquired:
                        return prop_acquired

                # Next in the "all" section of acquireds
                all_acquireds = acquireds.get('all')
                if all_acquireds:
                    prop_acquired = all_acquireds.get('template')
                    if prop_acquired:
                        return prop_acquired

        return templatename

    def __json__(self, resources):
        return dict(
            docname=self.docname,
            template=self.template(resources),
            repr=repr(self),
        )
