from kaybee_bulma.siteconfig import SiteConfig

import kaybee

# Sphinx setup
project = 'Kaybee'
version = kaybee.__version__
release = version
master_doc = 'index'
exclude_patterns = ['_build']
extensions = [
    'sphinx.ext.intersphinx',
    'kaybee',
    'kaybee_bulma',
]
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'sphinx': ('http://www.sphinx-doc.org/en/master', None),
    'dectate': ('http://dectate.readthedocs.io/en/latest', None),
}

# Theme setup
html_theme = 'kaybee_bulma'
html_static_path = ['_static']

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
    ]
}

kaybee_settings = kaybee.KaybeeSettings(
    articles=dict(
        use_toctree=True
    )
)

kaybee_bulma_siteconfig = SiteConfig(
    logo=dict(
        img_file='kaybee_logo.png',
        alt='Kaybee Logo Alt'
    ),
    copyright='2018, All Rights Reserved',
    favicon='kaybee_logo.png',
    social_media=dict(
        twitter='xxx',
        github='xxx'
    )
)
