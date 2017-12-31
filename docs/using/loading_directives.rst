==================
Loading Directives
==================

Kaybee is an extensible system. Your docs project, blog, website, intranet,
etc. can be written in terms of *your* kinds of things.

How do you extend Kaybee? With Python. Specifically, with directives, which
interact with some kind of :ref:`registry action <registry_action>`. For
example, your site might use ``kaybee_resources`` to define schema-validated
kinds of things. How do you define a "kind of thing"? With a Python directive
such as:

.. code-block:: python

    @kb.resource('invoice')
    class InvoiceResource(BaseResource)
        pass

That's great, but how does that line make something happen? There are several
ways to tell Kaybee to add directives to its configuration.

Directly in ``conf.py``
=======================


This is by far the simplest. Adding this in your conf file:

.. code-block:: python

    @kb.event(SphinxEvent.HPC)
    def add_context(kb_app, sphinx_app, pagename, templatename,
                    context, doctree):
        context['hello'] = 'world'

...results in the variable ``hello`` being added to the context in all Jinja2
templates.

Import Time
===========

Directives only need to be imported to get registered. Your ``conf.py`` can
import some of your code, some code in a package, etc. and Dectate (the
configuration framework used by Kaybee) will take the directive and process
its contents into configuration actions that are evaluated later.

If you have some code in your docs project (i.e. where your ``conf.py`` lies,
and your docs project isn't a proper Python package, then you'll have to
do a ``sys.path.insert`` dance to make your modules importable.

Local Plugins Dir
=================

Ah ha, Kaybee has anticipated this. If your docs project has a directory
called ``kaybee_plugins``, you can just put your modules in there and
Kaybee will import those files. Even better, it will do this import "later
on", which is code for "avoiding circular imports".

What if you have want a different name for the directory than
``kaybee_plugins``? There's a Kaybee setting for changing that directory
name.