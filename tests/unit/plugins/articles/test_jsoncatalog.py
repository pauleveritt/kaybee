import json

from plugins.articles.jsoncatalog import (
    generate_json_catalog,
    resources_to_json,
    references_to_json
)


class TestJsoncatalog:
    def test_imports(self):
        assert 'generate_json_catalog' == generate_json_catalog.__name__
        assert 'resources_to_json' == resources_to_json.__name__
        assert 'references_to_json' == references_to_json.__name__

    def test_resources_to_json(self, article_resources):
        result = resources_to_json(article_resources)
        assert 11 == len(result.keys())

    def test_references_to_json(self, article_resources, article_references):
        expected = dict(category=dict(c1=1), reference=dict())
        result = references_to_json(article_resources, article_references)
        c1 = result['category']['c1']

        assert 1 == c1['count']
        assert 'category/c1' == c1['docname']

    def test_generate_output(self, mocker,
                             kb_app, html_builder, sphinx_env,
                             article_resources, article_references):
        # Stash the resources and references on the environment
        sphinx_env.resources = article_resources
        sphinx_env.references = article_references

        # Make some mocks
        output_file = mocker.mock_open()
        mocker.patch('builtins.open', output_file, create=True)
        mocker.patch('json.dump')

        # Generate the JSON file
        generate_json_catalog(kb_app, html_builder, sphinx_env)

        # Test the filename written to
        filename = open.mock_calls[0][1][0]
        assert '/tmp/faker/catalog.json' == filename

        # Now test the results
        results = json.dump.mock_calls[0][1][0]
        resources = results['resources']
        assert 11 == len(resources.keys())
        references = results['references']
        c1 = references['category']['c1']

        assert 1 == c1['count']
        assert 'category/c1' == c1['docname']
