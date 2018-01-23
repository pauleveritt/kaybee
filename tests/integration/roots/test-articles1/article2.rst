.. article::
    category:
        - category1
        - category3

=========
Article 2
=========

Some body. This will have a querylist widget.

.. querylist::
    name: querylist1
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
