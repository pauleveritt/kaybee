from kaybee.plugins.genericpage.genericpage import Genericpage


class TestGenericpage:
    def test_import(self):
        assert 'Genericpage' == Genericpage.__name__

    def test_default_templatename(self, valid_gp, root_resource):
        # Nothing on the root resource, so use default templatename 'page'

        resources = dict(index=root_resource)
        templatename = valid_gp.template(resources)
        assert 'page' == templatename

    def test_root_no_acquireds(self, valid_gp, root_resource):
        # There's a root, but its props have no 'acquireds'
        resources = dict(index=root_resource)
        templatename = valid_gp.template(resources)
        assert 'page' == templatename

    def test_root_gp_no_templatename(self, valid_gp, root_resource):
        # Root acquireds with 'genericpage' section
        root_resource.props.acquireds = dict(flag=99)
        resources = dict(index=root_resource)
        templatename = valid_gp.template(resources)
        assert 'page' == templatename

    def test_root_gp_no_gp_templatename(self, valid_gp, root_resource):
        # Root acquireds with 'genericpage' section
        root_resource.props.acquireds = dict(
            genericpage=dict(flag=99)
        )
        resources = dict(index=root_resource)
        templatename = valid_gp.template(resources)
        assert 'page' == templatename

    def test_root_gp_templatename(self, valid_gp, root_resource):
        # Root acquireds with 'genericpage' section
        root_resource.props.acquireds = dict(
            genericpage=dict(template='gp_custom')
        )
        resources = dict(index=root_resource)
        templatename = valid_gp.template(resources)
        assert 'gp_custom' == templatename

    def test_root_all_no_alltemplatename(self, valid_gp, root_resource):
        # Root acquireds with 'all' section
        root_resource.props.acquireds = dict(
            all=dict(flag=99)
        )
        resources = dict(index=root_resource)
        templatename = valid_gp.template(resources)
        assert 'page' == templatename

    def test_root_all_no_templatename(self, valid_gp, root_resource):
        # Root acquireds with 'all' section
        root_resource.props.acquireds = dict(flag=99)
        resources = dict(index=root_resource)
        templatename = valid_gp.template(resources)
        assert 'page' == templatename

    def test_root_all_templatename(self, valid_gp, root_resource):
        # Root acquireds with 'all' section
        root_resource.props.acquireds = dict(
            all=dict(template='all_custom')
        )
        resources = dict(index=root_resource)
        tn = valid_gp.template(resources)
        assert 'all_custom' == tn

    def test_repr(self):
        # The repr is primarily useful in pytest listing
        br = Genericpage('somepage')
        assert 'somepage' == repr(br)

    def test_to_json(self, root_resource):
        root_resource.props.acquireds = dict(
            genericpage=dict(template='gp_custom')
        )
        resources = dict(index=root_resource)

        about = Genericpage('about')
        actual = about.__json__(resources)
        assert 'about' == actual['docname']
        assert 'gp_custom' == actual['template']
