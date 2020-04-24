from unittest import TestCase, expectedFailure
from unittest.mock import patch

from ..conference_client import GeneralConferenceClient, HTTPException

class ConferenceClientTests(TestCase):
    def setUp(self):
        self.get_patcher = patch('requests.get')
        self.addCleanup(self.get_patcher.stop)
        self.mock_get = self.get_patcher.start()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.text = (
            '<body><div><p>'
            '<span><a href="/general-conference/2019/04?lang=eng" class="year-line__link">April 2019</a></span'
            '<span><a href="/general-conference/2019/10?lang=eng">Skip This</a></span'
            '<span><a href="/general-conference/2019/10?lang=eng" class="year-line__link">October 2019</a></span'
            '</p></div></body>'
        )

        self.conf_client = GeneralConferenceClient('eng')

    def test_get_sessions(self):
        sessions = self.conf_client.get_sessions()
        self.assertEqual(2, len(sessions))
        self.assertEquals([()])
        self.mock_get.assert_called_once()
    

    def test_fail(self):
        self.mock_get.return_value.status_code = 400
        self.assertRaises(HTTPException, self.conf_client.get_sessions)