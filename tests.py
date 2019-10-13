from unittest import TestCase
from unittest.mock import patch

from sheepped import USPS, USPSError


class TestUSPS(TestCase):
    def setUp(self):
        self.usps = USPS("test-id")

    @patch("sheepped.requests.get")
    def test_successful_track(self, get):
        get.return_value.content = "<Response>Ok</Response>"
        self.assertEqual(self.usps.track("42"), {"Response": "Ok"})

    @patch("sheepped.requests.get")
    def test_failed_track(self, get):
        get.return_value.content = "<Error>Oops</Error>"
        with self.assertRaisesRegexp(USPSError, "Oops"):
            self.usps.track("42")
