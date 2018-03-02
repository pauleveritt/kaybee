.. article::
    published: 2018-01-02 12:01

========
Registry
========

Kaybee's plugin system makes it easy to extend in rich and interesting ways.

Kaybee provides a registry, based on
`Dectate <http://dectate.readthedocs.io>`_, which assembles configuration
that is processed once Sphinx starts its initializing. The registry provides
extensibility for docs projects, Kaybee plugins, and Kaybee itself.

.. _registry_action:

Actions
=======

Plugins can define new actions which let new kinds of things be registered
using directives. For example, ``kaybee_resources``, the most visible feature
of Kaybee, provides a new "resource" action in the registry. Projects can
then define new kinds of resources -- articles, authors, etc. -- using a
directive:

.. code-block:: python

    @kb.resource('article')
    class ArticleResource(BaseResource):
        pass

App
===

The example above has a decorator ``@kb``. What's ``kb``? In Dectate terms,
it is an app: a collection of configured actions, such as ``resource``.
Kaybee has a default app of ``kb``. But documentation projects can create
their own app with their own actions.

Discovery
=========

How do directives such as ``@kb.resource`` get located and processed? All
you have to do is import the module. The directive is added to the
configuration at import time. However, it isn't processed until later.
Specifically, during Sphinx's "builder init" event. This delay allows all
the bootstrapping to happen under Kaybee's control.

If you have lots of stuff to import, or for some reason don't want to manually
locate via import all the configuration, Kaybee ships with the
`importscan package <http://importscan.readthedocs.io>`_ which can do
imports via strings.
