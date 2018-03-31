.. section::
    style: light
    in_nav: True
    nav_title: Using
    weight: 20
    published: 2018-01-01 12:23
    is_series: True
    references:
        author:
            - paul
    acquireds:
        all:
            style: light

============
Using Kaybee
============

The :doc:`../features` document gave a high-level tour of using and
extending Kaybee. In this section we go into more depth on writing a
website using the core features of Kaybee.

.. querylist::
    name: ql1
    template: querylist
    queries:
        - label: Recent Blog Posts
          style: primary
          query:
              rtype: section
              limit: 5
        - label: Recent Articles
          style: info
          query:
              rtype: article
              limit: 5
.. toctree::
    :maxdepth: 2

    installation
    settings
    resources
    templates
    widgets
    references
    genericpage
    acquireds