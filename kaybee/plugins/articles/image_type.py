"""
pydantic field type for images.

Our resources have images associated with them. Not regular Sphinx images
which are part of the document. But rather, stuff associated with the
YAML, which we want to validate, post-process, and layout in our own
HTML.

"""
from pathlib import Path
import shutil

from pydantic import BaseModel
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.errors import SphinxError


class ImageModel(BaseModel):
    usage: str  # Multiple images can be attached so define usage
    filename: str

    def source_filename(self, docname: str, srcdir: str):
        """ Get the full filename to referenced image """

        docpath = Path(srcdir, docname)
        parent = docpath.parent
        imgpath = parent.joinpath(self.filename)

        # Does this exist?
        if not imgpath.exists():
            msg = f'Image does not exist at "{imgpath}"'
            raise SphinxError(msg)

        return imgpath

    def env_updated(self,
                    kb_app,
                    sphinx_app: Sphinx,
                    sphinx_env: BuildEnvironment,
                    resource
                    ):
        """ Make images and enter them in Sphinx's output writer """

        docname = resource.docname
        srcdir = sphinx_app.env.srcdir
        source_imgpath = self.source_filename(docname, srcdir)

        # Copy the image to the Sphinx build directory
        build_dir = sphinx_app.outdir
        docpath = Path(docname)
        parent = docpath.parent
        target_imgpath = str(Path(build_dir, parent, self.filename))
        shutil.copy(source_imgpath, target_imgpath)
