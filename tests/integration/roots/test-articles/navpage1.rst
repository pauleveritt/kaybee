.. navpage::
    entries:
        - docname: articles/index
        - docname: authors/index
          subheading: Do not use authors subheading
        - docname: categories/index
          label: Categories With Label
          query:
             rtype: resource
             limit: 5

=========
Navpage 1
=========

Some body.

                label=r.title,
                subheading=r.excerpt,
                docname=r.docname,
                accent='primary',
                icon='fas fa-eye'
