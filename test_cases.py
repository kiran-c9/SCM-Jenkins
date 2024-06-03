import os
import requests
import sys
import unittest
from mock import patch, MagicMock
from dotenv import load_dotenv


from jenkinspyscript import trigger_pipeline, get_logs, get_status

load_dotenv()


class TestJenkinsScript(unittest.TestCase):

    @patch('jenkinspyscript.requests.post')
    def test_trigger_pipeline(self, mock_post):

        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_post.return_value = mock_response

        result = trigger_pipeline()  
        self.assertTrue(result)

    
    
    @patch('jenkinspyscript.requests.get')
    def test_print_logs(self, mock_get):
        '''mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value ={'Got Logs':'Success'}
        mock_get.return_value = mock_response

        status = get_logs()
        self.assertEqual(status, 'SUCCESS')'''
       
        mock_get.side_effect = requests.exceptions.RequestException()        
        with self.assertRaises(requests.exceptions.RequestException):
            get_logs()

    @patch('jenkinspyscript.requests.get')
    def test_print_status(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'result': 'SUCCESS'}
        mock_get.return_value = mock_response

        status = get_status()
        self.assertEqual(status, 'SUCCESS')

    def test_handle_invalid_arguments(self):
        with self.assertRaises(SystemExit):
            with open('jenkinspyscript.py') as f:
                exec(compile(f.read(), 'jenkinspyscript.py', 'exec'))


if __name__ == '__main__':
    unittest.main()
