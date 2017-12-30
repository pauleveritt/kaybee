# Import each plugin, to process the directives

from importscan import scan
from kaybee.plugins import (
    events,
    localtemplates,
    resources
)

scan(resources)
