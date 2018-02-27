.. article::
    published: 2018-01-02 12:01

========
Settings
========

When your make a docs project, you need a way to supply some settings to
various pieces in Kaybee. Perhaps you want to turn on ``debugdump`` (a core
plugin.) Perhaps you want to supply your GitHub name for a Kaybee theme.

Each of these are settings. You choose a settings "model" -- the core model
from Kaybee itself, or a model from a Kaybee bundle, or your own settings
model that includes your plugins -- and give it some values.

Kaybee has a registered Sphinx configuration value of ``kaybee_settings``
that you use in the conf file. The object you provide here is available on
Sphinx's ``app`` object at ``sphinx.config``. Kaybee adds the Sphinx
``app`` object to the template environment, letting you insert a value in
your templates.

Using Settings
==============

#. In your docs project, import the settings model you'd like to use.

#. Assign an instance of this to the ``kaybee_settings`` config value.

#. Use the config value in an event handler. For example:

Here is an example of a ``conf.py`` file with basic settings.

   .. literalinclude:: ../../tests/integration/roots/test-settings/conf.py
