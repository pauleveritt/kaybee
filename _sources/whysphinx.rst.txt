==========
Why Sphinx
==========

If you're not in the world of Python, or if you don't use the wonderful
`ReadTheDocs <http://www.sphinx-doc.org/en/stable/>`_ site, then you might not
be familiar with Sphinx. Why is it a good basis for a KB system?

The Sphinx website and countless articles over the years cover this better
than we ever could. For the purposes of Kaybee, though, let's list a few
things.

Uh, Not Markdown?
=================

This is a deal-breaker for some. People hate learning another thing, and they
learned Markdown, and so they want Jekyll or Hugo or another system that
lets them write in ``.md`` files.

Sphinx uses a *very* similar system for encoding structure into plaintext
called `reStructuredText <http://docutils.sourceforge.net/rst.html>`_. It's
been around a long time. In fact, despite it being ``re`` of the original
"structured text", RST is older than Markdown by a good margin.

More importantly for Kaybee, RST is extensible. You can register new
directives, for example, which is critical for what Kaybee wants to do.

Either way, doesn't matter...Sphinx is what matters, Sphinx uses RST, so
there you go.

.. note::

    Yes, there are attempts to bring Markdown into Sphinx. But the story
    is iffy: loses much of the extensibility and isn't actively maintained
    relative to Sphinx.

Structural
==========

The first biggest thing that Sphinx provides vs. Jekyll and friends: it is
structural. It imagines your entire document set as an interlinked corpus,
from a heading to another file *in another remote project*. The linking is
rich, mature, useful, and validated...if you move something and break a
link, Sphinx tells you.

Since that happens a lot, Sphinx lets you link not to documents but targets
inside a document -- either auto-generated or a label that you put in.

Source Code
===========

When writing tech stuff, including source code is pretty useful. Sphinx was
first written for documentation, so it has gobs of facilities for this.
Not just the basics, but lots of stuff.

Extensibility
=============

Sphinx is old, which means mature, which means full-featured. It has adapted
to fulfill lots of needs.

One thing this translates to: lots of plug points. Want a custom "directive"?
Yep, you can do that. (The one thing that Markdown makes really difficult.)
Want a new kind of interlinking "reference" scheme? Yep. Need to run some
custom code on different events in the publishing pipeline? Yep. On and one.

Not Sphinx
==========

Kaybee aims to make it easier to work with Sphinx to build modern,
content-driven information sites. As such, some things change from what a
Sphinx person would expect.

Foremost, and this sucks...you can't do incremental builds. Pages are driven
by widgets and queries, not source-target nodes, so we can't tell Sphinx which
pages are dirty. At the moment, you can't even do the parallel-read thing.

At some point this will be rethought. Kaybee will try to pick the point
in the pipeline and retain some of the Sphinx environment state and pickle
information.