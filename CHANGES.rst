Changelog
=========


0.1.6 (2018-03-05)
------------------
- @WIP Let's release 0.1.6. [Paul Everitt]
- @WIP Screwed up the package ref. [Paul Everitt]
- @WIP Back to dev. [Paul Everitt]


0.1.5 (2018-03-05)
------------------

Changes
~~~~~~~
- References are now under a YAML node of ``references`` meaning you can
  extend the references scheme without having to write new models and
  thus make all-new types. [Paul Everitt]

Other
~~~~~
- @WIP Let's release 0.1.5. [Paul Everitt]
- @WIP Back to dev. [Paul Everitt]


0.1.4 (2018-03-02)
------------------
- @WIP Let's make 0.1.4. [Paul Everitt]
- @WIP Sigh, forgot to go back to dev. [Paul Everitt]


0.1.3 (2018-03-02)
------------------
- @WIP Release 0.1.3. [Paul Everitt]
- @WIP Fixed the PyPI credentials in .travis.yml. [Paul Everitt]
- @WIP Back to dev. Add in changelog. [Paul Everitt]


0.1.2 (2018-03-02)
------------------
- @WIP Let's make a PyPI release. [Paul Everitt]
- @WIP Trigger something that forces a rebuild. [Paul Everitt]
- @WIP PyPI has a decent release of kaybee_bulma now, try to use that.
  [Paul Everitt]
- @WIP More RTD wire wiggling. [Paul Everitt]
- @WIP Hmm, couldn't find the requirements.txt. [Paul Everitt]
- @WIP Maybe RTD now supports Python 3.6? [Paul Everitt]
- @WIP Improve the notes about release (and trigger Travis docs build.)
  [Paul Everitt]
- @WIP Don't speed up travis build with caching (looks like it broke.)
  [Paul Everitt]
- @WIP Speed up travis build with caching. [Paul Everitt]


0.1.1 (2018-03-02)
------------------
- @WIP Release 0.1.1. [Paul Everitt]
- @WIP Let's make a release. [Paul Everitt]


0.1.0 (2018-03-02)
------------------

New
~~~
- Built-in resource type ``resource`` which can be used in docs
  projects. [Paul Everitt]
- Extensible settings support. [Paul Everitt]

  Users can choose a KaybeSettings model as a configuration
  value in their conf.py. This model is made up of sub-models
  from the various plugins and system models that supply
  settings.
- Allow multiple handlers for same event with sorting using order. [Paul
  Everitt]

  Got rid of the "scope" positional argument when registering an event.
  It was used to allow multiple handlers for one event, overcoming
  Dectate's conflict resolution. You can now pass in nothing for the
  first registration and it defaults to 20. After that, you have to
  provide an "order" value to disambiguate, which also allows ordering
  of the handlers. 40-80 (on each event type) are reserved for the
  system.
- Implement remaining events. [Paul Everitt]
- Sphinx doctree read event. [Paul Everitt]
- Builder-init action. [Paul Everitt]

  Use a class method to handle the builder-init event and
  dispatch to any registered events. Increase code coverage.
- Add "event" action to the app. [Paul Everitt]

  This allows decorators such as @kb.event for each of the
  Sphinx events.
- Start a built-in registry app. [Paul Everitt]

  Provide implementation (empty), docs, and unit test. Also
  include Dectate in intersphinx. Provide some other docs.

Changes
~~~~~~~
- Introduce a featuretile widget which lays out Bulma tiles using YAML.
  [Paul Everitt]
- Feature section and lots more docs. [Paul Everitt]
- Clean up some orphans. [Paul Everitt]
- Nav_title can provide an alternate (shorter) label for a resource that
  appears in the nav. [Paul Everitt]
- Add some categories to the example documentation. [Paul Everitt]
- Series only shows up if parent flags it. [Paul Everitt]
- Use the toctree from kaybee_bulma. [Paul Everitt]
- Get directives with good dates sprinkled everywhere. Add acquired to
  sections to set colors. [Paul Everitt]
- Sprinkle some section directives into the mix. [Paul Everitt]
- Write tests that assert widget YAML models. [Paul Everitt]
- Re-arrange some wording. [Paul Everitt]
- Articles now have 3 flavors of settings for date formatting which work
  with a registered Jinja2 filter. [Paul Everitt]
- Dev; Make widget storage in the db unique by using the repr value
  instead of just the docname. (Also, stop using a deprecated value in
  the test.) [Paul Everitt]
- Strict mode with pydantic, complain if extra fields are supplied.
  [Paul Everitt]
- Section query. [Paul Everitt]
- Articles plugin now has working categories. [Paul Everitt]
- Add a querylist widget. Add featured_resource on sections. [Paul
  Everitt]
- Add a simple videoplayer widget. [Paul Everitt]
- Toctree works, now get series. [Paul Everitt]
- Let toctrees be registered in a way to override the builtin. [Paul
  Everitt]
- Out-of-the-box ready resource types. [Paul Everitt]

  Make tiny classes that can be decorated for article/homepage/section.
  Import them to get them registered, which means the integration test
  for acquired needed new names to avoid collision.
- Base homepage. [Paul Everitt]
- Change name of get_featured_resource and make a test. Move toctree to
  article. [Paul Everitt]
- Look for a template with the rtype/widget name instead of class name.
  [Paul Everitt]

  If the YAML didn't have (or acquire) a template name, we previously
  used the class name, lower cased. Make it clearer by using the rtype
  or wtype, meaning, the directive name.
- Stamp titles on resources during a handler. [Paul Everitt]
- Make an out-of-the-box reference type of "category". [Paul Everitt]
- Resource directives detect if the resource is a reference and if so,
  add the reference to sphinx_app.references. [Paul Everitt]

  Would be better if resources weren't responsible for this, and
  instead, have this happen in an event handler in references.
- Make an OOTB "widget" directive that can be used. [Paul Everitt]
- Increase test coverage. [Paul Everitt]
- Prove that ``genericpage`` is injected into template. [Paul Everitt]
- Put genericpage into html context. [Paul Everitt]
- Html-page-context handlers now have a protocol for letting the lambda
  return the template name string. [Paul Everitt]
- Integration tests for acquired properties. [Paul Everitt]
- Simplify existing test to use new __json__ instead of custom dumper.
  [Paul Everitt]
- Introduce "acquireds" as properties that can be gotten from parents.
  [Paul Everitt]
- Re-organized tests to be parameterized. [Paul Everitt]
- Get the sphinx_app into the HTML context. [Paul Everitt]
- Add some doc notes for resources work. [Paul Everitt]
- Event handler to add resource template directories to the Jinja2
  searchpath. [Paul Everitt]
- Add some info about using resources. [Paul Everitt]
- JSON serialization of a resource. [Paul Everitt]
- Beginnings of BaseResource: classes, parents, models. [Paul Everitt]
- Add some docs about import. [Paul Everitt]
- Configurable name for docs project kaybee_plugins directory. [Paul
  Everitt]

  By default it uses kaybee_plugins.
- Add specially-named docs project dir to path and import. [Paul
  Everitt]

  We need a way to scan for directives in the docs project without
  making the poor user do the sys.path.insert dance.
- Wrap the debugdump in a configuration value. [Paul Everitt]
- Make a note about how I do development (TDD, PyCharm). [Paul Everitt]
- Leave a note to document system. Simplify test setup. [Paul Everitt]
- Disambiguate system event handlers versus user event handlers. [Paul
  Everitt]
- Fix circular import with lambda to pass kb into dispatchers. [Paul
  Everitt]
- Explain how to load directives. [Paul Everitt]
- Writeup use of Dectate for a registry. [Paul Everitt]
- Better docs about setup. [Paul Everitt]
- Minimal notes about installation. [Paul Everitt]
- Introduce intersphinx and beef up dev docs. [Paul Everitt]
- Basic boilerplate copied over from previous repo. [Paul Everitt]

Other
~~~~~
- @WIP Let's make a release. [Paul Everitt]
- @WIP Let's make a release. [Paul Everitt]
- @WIP Some small docs changes. [Paul Everitt]
- @WIP Clean up todo. [Paul Everitt]
- @WIP Wire into app. [Paul Everitt]
- @WIP Put the code in the wrong files. [Paul Everitt]
- @WIP Clean todo. [Paul Everitt]
- @WIP Provide 3 articles settings for flavors of dates. [Paul Everitt]
- Update todo. [Paul Everitt]
- @WIP Integration tests pass for the image field. [Paul Everitt]
- @WIP Get the ImageModel and event handler unit tests working. [Paul
  Everitt]
- @WIP Let's do a checkpoint before fixing the docname. [Paul Everitt]
- @WIP pydantic model for copying images to output. [Paul Everitt]
- Let's see if we can push the docs on this bad boy. #2. [Paul Everitt]
- Let's see if we can push the docs on this bad boy. [Paul Everitt]
- Let sections have subheadings. [Paul Everitt]
- @WIP Pass the docname into load model to have nicer error reporting.
  [Paul Everitt]
- @WIP Switch from model to props: Model. [Paul Everitt]
- @WIP A hackety-hack shot at re-running the template generation on
  every run, to allow no re-parsing the doctrees. [Paul Everitt]
- @WIP All other stuff moved to environment. [Paul Everitt]
- @WIP Resources and references moved to env. [Paul Everitt]
- @WIP Simplify templates by putting resources and references into the
  Jinja2 context directly. [Paul Everitt]
- @WIP Update todos. [Paul Everitt]
- @WIP Section query tests with working parent_name. [Paul Everitt]
- @WIP Integration test for excerpt support. [Paul Everitt]
- @WIP Update the todo list. [Paul Everitt]
- @WIP Maybe use doctr for deploying docs to GH pages. [Paul Everitt]
- @WIP Wrong reference. [Paul Everitt]
- @WIP That's enough integration testing. [Paul Everitt]
- @WIP Test inline references. [Paul Everitt]
- @WIP Database -> postgresql. [Paul Everitt]
- @WIP Start of custom article reference. [Paul Everitt]
- @WIP Need to make the genericpage registration unique. [Paul Everitt]
- @WIP Genericpage. [Paul Everitt]
- @WIP Tests for built-in references. [Paul Everitt]
- Merge branch 'master' into custom_stuff. [Paul Everitt]

  # Conflicts:
  #	tests/integration/roots/test-kitchensink/kaybee_plugins/kitchensink_toctree.py
- @WIP Starter for base reference test case. [Paul Everitt]
- @WIP We have a new toctree entry so update test. Remove stray unused
  test file. [Paul Everitt]
- @WIP Custom resource and widget. [Paul Everitt]
- @WIP Custom article. [Paul Everitt]
- @WIP Add some testable droppings in toctree.html, wire up toctree, and
  write some tests. [Paul Everitt]
- @WIP Improve coverage. [Paul Everitt]
- @WIP Add test cases that go with kitchensink. [Paul Everitt]
- @WIP Add 70% of a kitchensink test site. [Paul Everitt]
- @WIP Increase test coverage. [Paul Everitt]
- @WIP Get querylist working with some tests. [Paul Everitt]
- @WIP BaseArticleReference and test. [Paul Everitt]
- @WIP Integration tests pass. [Paul Everitt]
- @WIP Change the built-in category to reference. [Paul Everitt]
- @WIP Bail out of the entire layouts idea. [Paul Everitt]
- @WIP Make a PIT commit before ripping out most of this. [Paul Everitt]
- @WIP Let's give it a better name. [Paul Everitt]
- @WIP Unit tests all pass. [Paul Everitt]
- @WIP Move more config to local conftest. [Paul Everitt]
- @WIP Move more config to local conftest. [Paul Everitt]
- @WIP Move most of the fake kb_app actions to local conftest. [Paul
  Everitt]
- @WIP Make is_published a property. Get back to 100% coverage. [Paul
  Everitt]
- @WIP Tests for layout action. [Paul Everitt]
- @WIP Better naming of the custom kb_app. [Paul Everitt]
- @WIP Re-organize genericpage unit tests to have a local kb_app. [Paul
  Everitt]
- @WIP Initial writeup. [Paul Everitt]
- @WIP More writing on resources. [Paul Everitt]
- @WIP Remove note about TODO. [Paul Everitt]
- @WIP Fix test now that series works. [Paul Everitt]
- @WIP Settings knob that turns off the injection of toctree. [Paul
  Everitt]
- @WIP Need a toctree template which mimics the existing builtin
  toctree. [Paul Everitt]
- @WIP Toctree template name needs suffix. [Paul Everitt]
- @WIP Not all resources have is_published. [Paul Everitt]
- @WIP Start of handler which finds the Sphinx toctrees and re-renders.
  [Paul Everitt]
- @WIP Multiple toctree registrations are making it through to the JSON
  dump tests. [Paul Everitt]
- @WIP BaseToctree with tests. [Paul Everitt]
- @WIP Register toctree on the kb registry. [Paul Everitt]
- @WIP Allow registering a context-specific (rtype) toctree. [Paul
  Everitt]
- @WIP Write integration tests for basics of articles. [Paul Everitt]
- @WIP Make some notes and add css_class as a prop. [Paul Everitt]
- @WIP Basics of articles in place. [Paul Everitt]
- @WIP Put the dumper handler "last" by giving it a high system_order.
  [Paul Everitt]

  Increase test coverage on rst utils.
- @WIP More todo gardening. [Paul Everitt]
- @WIP Leave a reminder. [Paul Everitt]
- @WIP Put resource_references hanging off of the ReferencesContainer.
  Add integration tests. [Paul Everitt]
- @WIP 100% coverage. [Paul Everitt]
- @WIP Finish the other handlers and write tests. [Paul Everitt]
- @WIP References actions and tests. [Paul Everitt]
- @WIP Skeleton of the references handlers etc. [Paul Everitt]
- @WIP Get integration tests to pass. [Paul Everitt]
- @WIP Last of the widget event handlers (although toctree is later.)
  [Paul Everitt]
- @WIP Implement and test base widget methods. [Paul Everitt]
- @WIP Register a handler that looks for widgets and replaces the
  contents with HTML. [Paul Everitt]
- @WIP Widget directive. [Paul Everitt]
- @WIP Basic layout of files and tests. [Paul Everitt]
- @WIP WidgetAction with tests. [Paul Everitt]
- @WIP Move the load_model to a central place to reuse across other
  plugins. [Paul Everitt]
- @WIP Remove comment. [Paul Everitt]
- @WIP Chaining. [Paul Everitt]
- @WIP Test pass with pydash individual functions, non-chained. [Paul
  Everitt]
- @WIP Essentially a copy-over of site.filter_resources. [Paul Everitt]
- @WIP Shell for query service. [Paul Everitt]
- @WIP Get genericpage actually into context. Fix bug returning
  template. [Paul Everitt]
- @WIP Remove unneeded fixture usage. [Paul Everitt]
- @WIP Add a type hint on return value. [Paul Everitt]
- @WIP documentation note. [Paul Everitt]
- Merge branch 'master' into resources-dict. [Paul Everitt]
- Merge branch 'master' into resources-dict. [Paul Everitt]

  # Conflicts:
  #	docs/implementation/index.rst
  #	docs/using/index.rst
  #	kaybee/plugins/__init__.py
- Initial commit. [Paul Everitt]


