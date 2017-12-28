import kaybee

version = kaybee.__version__
release = version
master_doc = 'index'
html_title = ''
exclude_patterns = ['_build']
html_theme = 'alabaster'
extensions = ['sphinx.ext.intersphinx', ]
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}
