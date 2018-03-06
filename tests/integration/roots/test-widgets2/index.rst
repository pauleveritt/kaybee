.. resource::

===========
Hello World
===========

.. listing::
    name: widgets1hello
    listing_flag: 98



    Here is some text.

    Here is some *more* text.

Not part of the widget.

.. querylist::
    name: ql1
    template: querylist
    queries:
        - label: Recent Stuff
          style: primary
          query:
              rtype: resource
              limit: 5
        - label: Template Uses Page
          style: info
          query:
              rtype: resource
              props:
                  - key: template
                    value: widgets2_resource1
              limit: 5

.. sectionquery::
    name: sectionquery1
    template: sectionquery
    query:
        rtype: resource


.. toctree::

    resource1