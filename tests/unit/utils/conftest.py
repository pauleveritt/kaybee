import pytest

from kaybee.utils.rst import (
    rst_document
)


@pytest.fixture()
def title_doc():
    source = '''\
=============
Test *Simple*
=============

Body       

    '''

    doc = rst_document(source)
    yield doc


@pytest.fixture()
def notitle_doc():
    source = '''\

Body       

    '''

    doc = rst_document(source)
    yield doc


@pytest.fixture()
def excerpt():
    source = """
Test
====

First *paragraph*.

Second *paragraph*.        
            """
    yield rst_document(source)


@pytest.fixture()
def noexcerpt():
    source = """
Test
====
            """
    yield rst_document(source)
