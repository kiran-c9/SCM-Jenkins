import os
import requests
import sys
import unittest
from mock import patch, MagicMock

# Importing functions from your script
from jenkinspyscript import trigger_pipeline, get_logs, get_status

class TestJenkinsScript(unittest.TestCase):
    @patch('jenkinspyscript.requests.post')
    def test_trigger_pipeline(self, mock_post):
        # Set up the mock Jenkins server and job
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        result = trigger_pipeline()  # No arguments needed
        self.assertTrue(result)

    
    @patch('jenkinspyscript.requests.post')
    def test_print_logs(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException()

        with self.assertRaises(requests.exceptions.RequestException):
            get_logs()

    @patch('jenkinspyscript.requests.get')
    def test_print_logs(self, mock_get):
        # Mocking a request exception
        mock_get.side_effect = requests.exceptions.RequestException()

        # Ensure that the function raises a RequestException
        with self.assertRaises(requests.exceptions.RequestException):
            get_logs()

    @patch('jenkinspyscript.requests.get')
    def test_print_status(self, mock_get):
        # Set up the mock Jenkins server and job
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'result': 'SUCCESS'}
        mock_get.return_value = mock_response

        status = get_status()
        self.assertEqual(status, 'SUCCESS')

    def test_handle_invalid_arguments(self):
        # Test invalid argument handling
        with self.assertRaises(SystemExit):
            # Call your function directly with invalid arguments
            sys.argv = ['test_cases.py', 'invalid-argument']
            exec(compile(open('jenkinspyscript.py').read(), 'jenkinspyscript.py', 'exec'))

if __name__ == '__main__':
    unittest.main()
