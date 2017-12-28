import kaybee

project = 'Kaybee'
version = kaybee.__version__
release = version
master_doc = 'index'
html_title = ''
exclude_patterns = ['_build']
html_theme = 'alabaster'
extensions = ['sphinx.ext.intersphinx', ]
pygments_style = 'sphinx'
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'sphinx': ('http://www.sphinx-doc.org', None),
}
