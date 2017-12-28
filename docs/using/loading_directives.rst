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

That's great, but how does that line make something happen? There are two
ways to tell Kaybee to add directives to its configuration.

Import Time
===========

This is the simplest and most obvious. In your ``docs/conf.py`` file, simply
import the module with the directive. That's all it takes. Dectate (the
configuration framework used by Kaybee) will take the directive and process
its contents into configuration actions that are evaluated later.

.. note::

    Sphinx supports a ``setup`` function in your ``docs/conf.py`` file. This
    would let you defer the importing until later, that is, when Sphinx
    processes extensions.

importscan
==========

You might have a reason to not want to use imports: lots of extra lines, or
your actions have some sequencing that needs to be handled manually. Kaybee
ships with ``importscan`` which has rich facilities for wildcard-string-based
imports.