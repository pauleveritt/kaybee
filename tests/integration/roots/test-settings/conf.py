import os
import sys

import kaybee

sys.path.insert(0, os.path.abspath('.'))
# noinspection PyUnresolvedReferences
import kaybee_plugins

extensions = [kaybee.__title__]

master_doc = 'index'
html_title = ''
exclude_patterns = ['_build']

kaybee_settings = kaybee.KaybeeSettings(
    debugdumper=dict(
        use_debug=True
    )
)
