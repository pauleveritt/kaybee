import pytest
from sphinx.application import Sphinx
from sphinx.errors import SphinxError
from sphinx.util import FilenameUniqDict

from kaybee.plugins.articles.image_type import ImageModel
from kaybee.utils.models import load_model
from kaybee.plugins.articles.base_article import BaseArticle


@pytest.fixture()
def image_model():
    yaml = """
    filename: img.png
            """
    im: ImageModel = load_model('somedoc', ImageModel, yaml)

    yield im


@pytest.fixture()
def image_sphinx_app(sphinx_app):
    sphinx_app.env.srcdir = '/tmp'
    sphinx_app.env.images = FilenameUniqDict()

    yield sphinx_app


class TestImageModel:
    def test_import(self):
        assert 'ImageModel' == ImageModel.__name__

    def test_construction(self, image_model: ImageModel):
        assert 'img.png' == image_model.filename

    def test_edr_valid_path(self,
                            mocker,
                            image_sphinx_app: Sphinx,
                            dummy_article: BaseArticle,
                            image_model: ImageModel):
        mocker.patch.object(image_sphinx_app.env.images, 'add_file')
        result = image_model.env_doctree_read(image_sphinx_app, {},
                                              dummy_article)
        docname, imgpath = image_sphinx_app.env.images.add_file.call_args[0]
        assert dummy_article.docname == docname

    def test_edr_invalid_path(self, image_sphinx_app: Sphinx,
                              dummy_article: BaseArticle,
                              image_model: ImageModel):
        image_model.filename = 'faker.png'
        with pytest.raises(SphinxError):
            image_model.env_doctree_read(image_sphinx_app, {},
                                              dummy_article)
