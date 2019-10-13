from os import environ
from unittest import TestCase
from unittest.mock import patch

from asynctest import TestCase as AioTestCase, CoroutineMock, patch as aiopatch

from sheepped import USPS, USPSError


class TestUSPSInit(TestCase):
    def setUp(self):
        self.saved_id = None
        if "USPS_USER_ID" in environ:
            self.saved_id = environ["USPS_USER_ID"]
            del environ["USPS_USER_ID"]

    def tearDown(self):
        if self.saved_id:
            environ["USPS_USER_ID"] = self.saved_id

    def test_no_user_id(self):
        with self.assertRaisesRegex(
            USPSError, "No USPS ID passed or envvar USPS_USER_ID set."
        ):
            self.usps = USPS()

    def test_no_envvar_but_user_id_informed(self):
        usps = USPS("test-id")
        self.assertIn("test-id", usps.url_for("42"))

    def test_no_user_id_informed_but_envvar_set(self):
        environ["USPS_USER_ID"] = "test-id"
        usps = USPS()
        self.assertIn("test-id", usps.url_for("42"))

    def test_user_id_informed_and_envvar_set_results_in_informed(self):
        environ["USPS_USER_ID"] = "test-envvar-id"
        usps = USPS("test-informed-id")
        self.assertIn("test-informed-id", usps.url_for("42"))
        self.assertNotIn("test-envvar-id", usps.url_for("42"))


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
