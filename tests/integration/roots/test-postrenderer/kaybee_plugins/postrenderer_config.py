from kaybee.app import kb


@kb.postrenderer('capitalize')
class CapitalizePostrenderer:
    def __call__(self, html, context):
        # This is a shim because integration tests all run with same
        # damn registry.
        if 'capitalizemeplease' in html:
            return html.upper()
        return html
