import kaybee
import sys
sys.path.append('.')
from kaybee_plugins.layout_mylayout1 import MyLayout1

extensions = [kaybee.__title__]

master_doc = 'index'
html_title = ''
exclude_patterns = ['_build']
html_theme = MyLayout1(
    copyright=2999
)

kaybee_settings = kaybee.KaybeeSettings(
    debugdumper=dict(
        use_debug=True
    )
)
