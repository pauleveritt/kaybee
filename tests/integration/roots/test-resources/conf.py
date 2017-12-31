import kaybee

extensions = [kaybee.__title__]

master_doc = 'index'
html_title = ''
exclude_patterns = ['_build']


kaybee_settings = kaybee.KaybeeSettings(
    debugdumper=dict(
        use_debug=True
    )
)
