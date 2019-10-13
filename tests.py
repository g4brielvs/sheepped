from unittest import TestCase
from unittest.mock import patch

from asynctest import TestCase as AioTestCase, CoroutineMock, patch as aiopatch

from sheepped import USPS, USPSError


class BaseTestCase:
    EXPECTED_URL = (
        "https://secure.shippingapis.com/ShippingAPI.dll?API=TrackV2&XML="
        '<TrackFieldRequest USERID="test-id">'
        '<TrackID ID="42"/>'
        "</TrackFieldRequest>"
    )

    def setUp(self):
        self.usps = USPS("test-id")


class TestUSPS(BaseTestCase, TestCase):
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


class TestAioUSPS(BaseTestCase, AioTestCase):
    @aiopatch("aiohttp.ClientSession.get")
    async def test_successful_aiotrack(self, get):
        get.return_value.__aenter__.return_value.read = CoroutineMock(
            return_value=b"<Response>Ok</Response>"
        )
        response = await self.usps.aiotrack("42")
        self.assertEqual(response, {"Response": "Ok"})
        get.assert_called_once_with(self.EXPECTED_URL)

    @aiopatch("aiohttp.ClientSession.get")
    async def test_failed_aiotrack(self, get):
        get.return_value.__aenter__.return_value.read = CoroutineMock(
            return_value=b"<Error>Oops</Error>"
        )
        with self.assertRaisesRegex(USPSError, "Oops"):
            await self.usps.aiotrack("42")
        get.assert_called_once_with(self.EXPECTED_URL)
