from flask_testing import TestCase
import app

class BaseTestCase(TestCase):
    """Base Test Case class."""

    def create_app(self):
        test_app = app.create_app({'TESTING': True})
        return test_app