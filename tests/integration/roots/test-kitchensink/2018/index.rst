.. section::
    featured_resource: 2018/ksarticle1

=============
2018 Articles
=============

First, a video.


Section Query
=============

.. querylist::
    name: querylist1
    template: querylist
    queries:
        - label: Recent Sections
          style: primary
          query:
              rtype: section
              limit: 5
        - label: Recent Articles
          style: info
          query:
              rtype: article
              limit: 5

Contents
========

.. toctree::

    intro_django
    just_a_resource
    ksresource1
    ksarticle1