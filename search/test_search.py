from test_base import BaseTestCase
from flask import url_for
from unittest.mock import Mock, patch
from search import search

class HomeViewTestCase(BaseTestCase):
    """Class to test home view."""

    def test_the_template_used_for_the_view(self):
        """Test correct template used."""
        self.client.get(url_for('search.result'))

        self.assertTemplateUsed('/search/result.html')

    def test_correct_url_returned_from_url_for_function(self):
        """Test that the correct url is returned from the from_url() function."""
        url = url_for('search.result')

        self.assertEqual(url, '/search')
    
    def test_template_context_without_an_address_parameter(self):
        """Test template context when address is not present."""
        url = url_for('search.result')

        self.client.get(url)

        self.assertContext(
            "context",
            {
                "address": None,
                "found": False,
                "searched": False
            }
        )
    
    def test_template_context_with_an_empty_address_parameter(self):
        """Test template context when address parameter is empty"""
        url = url_for("search.result")

        url = url + "?address="
        self.client.get(url)

        self.assertContext(
            "context",
            {
                "address": "",
                "found": False,
                "searched": False
            }
        )

    def test_template_rendered_when_address_parameter_empty(self):
        """Test template rendered when address argument is empty"""
        url = url_for('search.result')

        response = self.client.get(url)

        self.assertStatus(response, 200)
        self.assertIn("Invalid Search.", str(response.data))

    def test_template_rendered_with_results_for_a_valid_address_parameter(self):
        """Test response when a known valid address parameter is passed.
        In this case the address parameter passed in is "Moscow Ring Road"
        """
        url = url_for("search.result")
        url = url + "?address=Moscow+Ring+Road"

        response = self.client.get(url)

        context = self.get_context_variable("context")

        results = context["results"]

        self.assertStatus(response, 200)
        self.assertIn("Results for <strong>Moscow Ring Road</strong>", str(response.data))
        self.assertEqual(context["ok"], True)
        self.assertEqual(context["found"], True)
        self.assertEqual(context["searched"], True)
        self.assertTrue(len(results) > 0)
        self.assertTrue("name" in results[0])
        self.assertTrue("longitude" in results[0])
        self.assertTrue("latitude" in results[0])
    
    def test_template_rendered_without_results_for_a_valid_address_parameter(self):
        """Test response when a valid address parameter is passed, but no results
        were found.
        """
        url = url_for("search.result")
        url = url + "?address=Udo+Ebitus+Street"

        response = self.client.get(url)

        context = self.get_context_variable("context")

        self.assertStatus(response, 200)
        self.assertIn("Results for <strong>Udo Ebitus Street</strong>", str(response.data))
        self.assertIn("No Results Found.", str(response.data))
        self.assertEqual(context["ok"], True)
        self.assertEqual(context["found"], False)
        self.assertEqual(context["searched"], True)

    def test_template_rendered_with_failed_response_for_a_valid_address_parameter(self):
        """Test template rendered for a valid address parameter, with known valid results
        but request to the api fails due to some reasons such as no network access or
        invalid response.
        """
        url = url_for("search.result")
        url = url + "?address=Moscow+Ring+Road"
        mock_geo_code = Mock(name="geo_code")
        mock_geo_code.return_value = {
            "ok": False,
            "found": False,
            "searched": True
        }

        with patch.object(search, 'geo_code', mock_geo_code):
            response = self.client.get(url)
            context = self.get_context_variable("context")

            self.assertStatus(response, 200)
            self.assertIn("Search Error, Try Again.", str(response.data))
            self.assertEqual(context["ok"], False)
            self.assertEqual(context["found"], False)
            self.assertEqual(context["searched"], True)
            mock_geo_code.assert_called_once()
            mock_geo_code.assert_called_once_with("Moscow+Ring+Road")

