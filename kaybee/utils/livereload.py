"""

Automatically re-build Sphinx docs while editing, serve docs on an
HTTP port, and also reload any browsers pointed to the docs.

"""

import glob
import sys
from pathlib import PurePosixPath

from livereload import Server, shell
from livereload.watcher import Watcher


class CustomWatcher(Watcher):
    """ Handle recursive globs with Python 3.5+ globbing  """

    paths = [
        'docs/**',
        'kaybee/**.py'
    ]
    root = 'docs/_build'

    def __init__(self):
        super().__init__()
        self.interp = sys.executable
        self.sphinx = str(PurePosixPath(self.interp).parent / 'sphinx-build')
        self.cmd = f'{self.interp} {self.sphinx} -E -b html docs docs/_build'

    def is_glob_changed(self, path, ignore=None):
        for f in glob.glob(path, recursive=True):
            if self.is_file_changed(f, ignore): # pragma: no cover
                return True
        return False


if __name__ == '__main__': # pragma: no cover
    watcher = CustomWatcher()
    server = Server(watcher=CustomWatcher())
    for p in watcher.paths:
        server.watch(p, shell(watcher.cmd),
                     ignore=lambda s: '_build' in s)
    server.serve(root=watcher.root, live_css=False)
