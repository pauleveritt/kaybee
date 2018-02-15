import shutil
from inspect import getfile
from pathlib import Path

import pytest
from sphinx.application import Sphinx
from sphinx.errors import SphinxError
from sphinx.util import FilenameUniqDict

from kaybee.plugins.articles.base_article import BaseArticle
from kaybee.plugins.articles.image_type import ImageModel
from kaybee.utils.models import load_model


@pytest.fixture()
def image_model():
    yaml = """
    usage: teaser
    filename: img.png
            """
    im: ImageModel = load_model('somedoc', ImageModel, yaml)

    yield im


@pytest.fixture()
def get_module_dir():
    # Need to get path to image in this tests's directory
    gf = getfile(get_module_dir)
    yield Path(gf).parent


@pytest.fixture()
def image_sphinx_app(sphinx_app, get_module_dir):
    sphinx_app.env.srcdir = get_module_dir
    sphinx_app.env.images = FilenameUniqDict()

    yield sphinx_app


class TestImageModel:
    def test_import(self):
        assert 'ImageModel' == ImageModel.__name__

    def test_construction_exists(self, image_model: ImageModel):
        assert 'img.png' == image_model.filename

    def test_valid_source_filename(self, image_sphinx_app: Sphinx,
                                   image_model: ImageModel):
        docname = 'index'
        imgpath = image_model.source_filename(docname,
                                              image_sphinx_app.env.srcdir)
        assert str(imgpath).endswith('unit/plugins/articles/img.png')

    def test_invalid_source_filename(self, image_sphinx_app: Sphinx,
                                     image_model: ImageModel):
        docname = 'f1/f2/about'
        with pytest.raises(SphinxError):
            image_model.source_filename(docname,
                                        image_sphinx_app.env.srcdir)

    def test_env_updated(self,
                         mocker,
                         kb_app,
                         image_sphinx_app: Sphinx,
                         dummy_article: BaseArticle,
                         image_model: ImageModel):
        mocker.patch('shutil.copy')
        dummy_article.docname = 'index'
        imgpath = image_model.source_filename(dummy_article.docname,
                                              image_sphinx_app.env.srcdir)
        image_sphinx_app.env.outdir = '/tmp'
        result = image_model.env_updated(
            kb_app,
            image_sphinx_app,
            image_sphinx_app.env,
            dummy_article
        )
        shutil.copy.assert_called_once_with(
            imgpath, '/tmp/img.png'
        )

    def test_edr_invalid_path(self,
                              kb_app,
                              image_sphinx_app: Sphinx,
                              dummy_article: BaseArticle,
                              image_model: ImageModel):
        image_model.filename = 'faker.png'
        with pytest.raises(SphinxError):
            image_model.env_updated(kb_app, image_sphinx_app, {},
                                    dummy_article)
