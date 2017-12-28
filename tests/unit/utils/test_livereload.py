from kaybee.utils.livereload import CustomWatcher


class TestLivereload:
    def test_interpreter_path(self):
        cw = CustomWatcher()
        assert 'python' in cw.interp
        assert 'sphinx-build' in cw.sphinx

    def test_is_glob_changed(self):
        cw = CustomWatcher()
        result = cw.is_glob_changed('.')
        assert not result
