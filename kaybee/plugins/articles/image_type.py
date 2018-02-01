"""
pydantic field type for images.

Our resources have images associated with them. Not regular Sphinx images
which are part of the document. But rather, stuff associated with the
YAML, which we want to validate, post-process, and layout in our own
HTML.

"""
from os import path

from docutils.readers import doctree
from docutils.utils import relative_path
from pydantic import BaseModel
from sphinx.application import Sphinx
from sphinx.errors import SphinxError


class ImageModel(BaseModel):
    filename: str

    def env_doctree_read(self, sphinx_app: Sphinx, doctree: doctree, resource):
        """ Make images and enter them in Sphinx's output writer """
        docname = resource.docname
        img_filename = self.filename
        imgpath = relative_path(
            path.join(sphinx_app.env.srcdir, docname),
            img_filename)

        # Does this exist?
        if not path.exists(imgpath):
            msg = f'Image does not exist at "{imgpath}"'
            raise SphinxError(msg)

        # Add this to the list of files to copy out
        sphinx_app.env.images.add_file(docname, imgpath)
