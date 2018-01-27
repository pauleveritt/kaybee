import kaybee

extensions = [kaybee.__title__]

master_doc = 'index'
html_title = ''
exclude_patterns = ['_build']
project = 'Kitchen Sink'

# Theme setup
html_theme = 'alabaster'

html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
    ]
}

kaybee_settings = kaybee.KaybeeSettings(
    debugdumper=dict(
        use_debug=True
    ),
    articles=dict(
        use_toctree=True
    )
)
