import re
from werkzeug.utils import escape
from werkzeug.wrappers import response
from search.search import result
from test_base import BaseTestCase
from flask import url_for

class CalculateTestCase(BaseTestCase):
    """Test Class for calculate view and calculate_distance method."""

    def test_url_for_the_view(self):
        """Test for correct url string for the view."""
        url = url_for("calculate.calculate")

        self.assertEqual(url, "/calculate")

    def test_correct_template_is_rendered(self):
        """Test for correct template rendered."""
        url = url_for("calculate.calculate")

        self.client.get(url)

        self.assertTemplateUsed("/calculate/calculate.html")

    def test_for_location_within_mkad(self):
        """Test template response when searched location is within the mkad boundary."""
        url = url_for("calculate.calculate")
        url = url  + "?lat=55.766557&lon=37.623429&name=Russia,%20Moscow,%20Boulevard%20Ring"

        response = self.client.get(url)

        self.assertStatus(response, 200)
        self.assertIn("Location is within MKAD", str(response.data))
        self.assertContext(
            "context",
            {
                'distance': -1, 
                'success': True, 
                'longitude': '37.623429', 
                'latitude': '55.766557', 
                'name': 'Russia, Moscow, Boulevard Ring'
            }
        )

    def test_for_location_outside_mkad_without_name_argument(self):
        """Test for a location that is outside the mkad boundary."""
        url = url_for("calculate.calculate")
        url = url  + "?lat=55.821072&lon=37.837153"

        response = self.client.get(url)

        self.assertStatus(response, 200)
        self.assertIn("Lat: 55.821072", str(response.data))
        self.assertIn("Lon: 37.837153", str(response.data))
        self.assertIn("Moscow Ring Road", str(response.data))
        self.assertIn("16.41 km", str(response.data))
        self.assertContext(
            "context",
            {
                'distance': 16.41, 
                'success': True, 
                'longitude': '37.837153', 
                'latitude': '55.821072', 
                'name': None
            }
        )

    def test_for_location_on_the_mkad_boundary(self):
        """Test for a location on the boundary's edge."""
        url = url_for("calculate.calculate")
        url = url  + "?lat=55.747399&lon=37.841828"

        response = self.client.get(url)

        self.assertStatus(response, 200)
        self.assertIn("Lat: 55.747399", str(response.data))
        self.assertIn("Lon: 37.841828", str(response.data))
        self.assertIn("Moscow Ring Road", str(response.data))
        self.assertIn("14.36 km", str(response.data))
        self.assertContext(
            "context",
            {
                'distance': 14.36, 
                'success': True, 
                'longitude': '37.841828', 
                'latitude': '55.747399', 
                'name': None
            }
        )

    def test_when_invalid_valid_input_is_passed_as_longitude_only(self):
        """Test when invalid input is passed to the view."""
        url = url_for("calculate.calculate")
        url = url  + "?lat=55.747399&lon=invalid"

        response = self.client.get(url)

        self.assertStatus(response, 200)
        self.assertIn(
            "Error in Latitude and/or Longitude values, ex. 58.34553234 .", 
            str(response.data)
        )
        self.assertContext(
            "context",
            {
                'distance': 0, 
                'success': False, 
                'longitude': 'invalid', 
                'latitude': '55.747399', 
                'name': None
            }
        )


    def test_when_no_arguments_is_passed(self):
        """Test when no value is passed."""
        url = url_for("calculate.calculate")
        url = url  + "?lat=invalid&lon=37.841828"

        response = self.client.get(url)

        self.assertStatus(response, 200)
        self.assertIn(
            "Error in Latitude and/or Longitude values, ex. 58.34553234 .", 
            str(response.data)
        )
        self.assertContext(
            "context",
            {
                'distance': 0, 
                'success': False, 
                'longitude': '37.841828', 
                'latitude': 'invalid', 
                'name': None
            }
        ) 

    def test_when_invalid_valid_input_is_passed_as_latitude_only(self):
        """Test when invalid input is passed to the view."""
        url = url_for("calculate.calculate")
        url = url  + "?lat=invalid&lon=37.841828"

        response = self.client.get(url)

        self.assertStatus(response, 200)
        self.assertIn(
            "Error in Latitude and/or Longitude values, ex. 58.34553234 .", 
            str(response.data)
        )
        self.assertContext(
            "context",
            {
                'distance': 0, 
                'success': False, 
                'longitude': '37.841828', 
                'latitude': 'invalid', 
                'name': None
            }
        ) 

    def test_when_both_values_are_invalid(self):
        """Test when both parameters passed to the view is invalid."""
        url = url_for("calculate.calculate")
        url = url  + "?lat=invalid&lon=invalid"

        response = self.client.get(url)

        self.assertStatus(response, 200)
        self.assertIn(
            "Error in Latitude and/or Longitude values, ex. 58.34553234 .", 
            str(response.data)
        )
        self.assertContext(
            "context",
            {
                'distance': 0, 
                'success': False, 
                'longitude': 'invalid', 
                'latitude': 'invalid', 
                'name': None
            }
        ) 

    def test_when_no_value_is_passed_for_longitude_only(self):
        """Test when there is no longitude value."""
        url = url_for("calculate.calculate")
        url = url  + "?lat=57.3445&lon="

        response = self.client.get(url)

        self.assertStatus(response, 200)
        self.assertIn(
            "Error in Latitude and/or Longitude values, ex. 58.34553234 .", 
            str(response.data)
        )
        self.assertContext(
            "context",
            {
                'distance': 0, 
                'success': False, 
                'longitude': '', 
                'latitude': '57.3445', 
                'name': None
            }
        )  

    def test_when_no_value_is_passed_for_latitude_only(self):
        """Test when there is no latitude value."""
        url = url_for("calculate.calculate")
        url = url  + "?lat=&lon=57.3445"

        response = self.client.get(url)

        self.assertStatus(response, 200)
        self.assertIn(
            "Error in Latitude and/or Longitude values, ex. 58.34553234 .", 
            str(response.data)
        )
        self.assertContext(
            "context",
            {
                'distance': 0, 
                'success': False, 
                'longitude': '57.3445', 
                'latitude': '', 
                'name': None
            }
        )  

    def test_when_both_arguments_are_ommited(self):
        """Test when there are no arguments passed in."""
        url = url_for("calculate.calculate")
        url = url  + "?"

        response = self.client.get(url)

        self.assertStatus(response, 200)
        self.assertIn(
            "Error in Latitude and/or Longitude values, ex. 58.34553234 .", 
            str(response.data)
        )
        self.assertContext(
            "context",
            {
                'distance': 0, 
                'success': False, 
                'longitude': None, 
                'latitude': None, 
                'name': None
            }
        ) 
    
    def test_logging_was_done_when_a_location_tested_is_out_of_the_mkad_boundary(self):
        """Test logging functionality."""
        url = url_for("calculate.calculate")
        url = url  + "?lat=55.821072&lon=37.837153"

        log_info_before_request = self.read_log_file_info()

        response = self.client.get(url)

        log_info_after_request = self.read_log_file_info()

        self.assertEqual(log_info_before_request["count"] + 1, log_info_after_request["count"])
        self.assertNotEqual(
            log_info_after_request["last_line"], 
            log_info_before_request["last_line"]
        )


        # Create a regex to match and verify the log message sent to the file.
        pattern = (
            r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}\]"
            + r" INFO in calculate: Distance from Lat: 55.821072 \| Lon: 37.837153"
            + r" to Moscow Ring Road: 16.41km ."""
        )

        match = re.match(pattern, log_info_after_request["last_line"])

        self.assertFalse(match is None)

        self.assertStatus(response, 200)
        self.assertIn("Lat: 55.821072", str(response.data))
        self.assertIn("Lon: 37.837153", str(response.data))
        self.assertIn("Moscow Ring Road", str(response.data))
        self.assertIn("16.41 km", str(response.data))
        self.assertContext(
            "context",
            {
                'distance': 16.41, 
                'success': True, 
                'longitude': '37.837153', 
                'latitude': '55.821072', 
                'name': None
            }
        )

    def test_logging_is_not_done_when_a_location_tested_is_within_the_mkad_boundary(self):
        """Testing logging is not done when the searched location is within the mkad."""
        url = url_for("calculate.calculate")
        url = url  + "?lat=55.766557&lon=37.623429&name=Russia,%20Moscow,%20Boulevard%20Ring"

        log_info_before_request = self.read_log_file_info()

        response = self.client.get(url)

        log_info_after_request = self.read_log_file_info()

        self.assertEqual(log_info_after_request["count"], log_info_before_request["count"])
        self.assertEqual(
            log_info_after_request["last_line"], 
            log_info_before_request["last_line"]
        )

        self.assertStatus(response, 200)
        self.assertIn("Location is within MKAD", str(response.data))
        self.assertContext(
            "context",
            {
                'distance': -1, 
                'success': True, 
                'longitude': '37.623429', 
                'latitude': '55.766557', 
                'name': 'Russia, Moscow, Boulevard Ring'
            }
        )
    
    def read_log_file_info(self) -> dict:
        """Return the number of lines and last line of the log file "app.log" ."""
        line_count = 0
        last_line = None

        try:
            stream = open("app.log", "rt")
            for line in stream:
                line_count += 1
                last_line = line
            stream.close()
        except:
            pass

        return {"count": line_count, "last_line": last_line}


