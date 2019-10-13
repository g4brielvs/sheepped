from unittest import TestCase
from unittest.mock import patch

from sheepped import USPS, USPSError


class TestUSPS(TestCase):
    EXPECTED_URL = (
        "https://secure.shippingapis.com/ShippingAPI.dll?API=TrackV2&XML="
        '<TrackFieldRequest USERID="test-id">'
        '<TrackID ID="42"/>'
        "</TrackFieldRequest>"
    )

    def setUp(self):
        self.usps = USPS("test-id")

    @patch("sheepped.requests.get")
    def test_successful_track(self, get):
        get.return_value.content = b"<Response>Ok</Response>"
        response = self.usps.track("42")
        self.assertEqual(response, {"Response": "Ok"})
        get.assert_called_once_with(self.EXPECTED_URL)

    @patch("sheepped.requests.get")
    def test_failed_track(self, get):
        get.return_value.content = b"<Error>Oops</Error>"
        with self.assertRaisesRegex(USPSError, "Oops"):
            self.usps.track("42")
        get.assert_called_once_with(self.EXPECTED_URL)
