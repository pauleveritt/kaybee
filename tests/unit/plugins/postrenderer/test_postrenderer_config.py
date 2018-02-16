from kaybee.plugins.postrenderer.config import (
    KaybeeBridge,
)


class TestPostrenderConfig:
    def test_import(self):
        assert 'KaybeeBridge' == KaybeeBridge.__name__

    def test_construction(self):
        bridge = KaybeeBridge()
        assert hasattr(bridge, 'render')

    def test_one_renderer(self,
                          mocker,
                          postrenderer_kb_app,
                          register_valid_event):
        output = '<p>hello</p>'

        def r(instance, template, context):
            return output

        mocker.patch('sphinx.jinja2glue.BuiltinTemplateLoader.render', r)
        bridge = KaybeeBridge()
        mocker.patch.object(bridge, 'get_kb', return_value=postrenderer_kb_app)
        result = bridge.render('', dict())
        assert '<P>HELLO</P>' == result

    def test_two_renderers(self,
                           mocker,
                           postrenderer_kb_app,
                           register_two_valid_events):
        output = '<p>hello</p>'

        def r(instance, template, context):
            return output

        mocker.patch('sphinx.jinja2glue.BuiltinTemplateLoader.render', r)
        bridge = KaybeeBridge()
        mocker.patch.object(bridge, 'get_kb', return_value=postrenderer_kb_app)
        result = bridge.render('', dict())
        assert '<DIV>LOREM IPSUM</DIV>' == result
