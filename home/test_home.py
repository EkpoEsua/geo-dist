from test_base import BaseTestCase
from flask import url_for


class HomeViewTestCase(BaseTestCase):
    """Test Cases for the home view."""

    def test_template_used_for_home_view(self):
        """Test the template used to render the home view."""
        response = self.client.get(url_for('home.index'))

        self.assertTemplateUsed('/home/home.html')

    def test_correct_url_returned_from_url_for_function(self):
        """Test that the correct url is returned from the from_url() function."""
        url = url_for('home.index')

        self.assertEqual(url, '/')