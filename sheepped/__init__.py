from os import getenv

import requests
import xmltodict
from aiohttp import ClientSession
from lxml import etree


class USPSError(Exception):
    pass


class USPS:
    """
    Wrapper around USPS tracking API
    :param str user_id: USPS User ID
    """

    URL = "https://secure.shippingapis.com/ShippingAPI.dll?API=TrackV2&XML="

    def __init__(self, user_id=None):
        if not user_id and not getenv("USPS_USER_ID"):
            raise USPSError("No USPS ID passed or envvar USPS_USER_ID set.")
        self.user_id = user_id or getenv("USPS_USER_ID")

    def url_for(self, tracking_number):
        xml = etree.Element("TrackFieldRequest", {"USERID": self.user_id})
        etree.SubElement(xml, "TrackID", {"ID": tracking_number})
        value = etree.tostring(xml).decode()
        return f"{self.URL}{value}"

    def parse_xml_response(self, xml_response):
        response = xmltodict.parse(xml_response)
        if "Error" in response:
            raise USPSError(response["Error"])
        return response

    def track(self, tracking_number):
        url = self.url_for(tracking_number)
        contents = requests.get(url).content
        return self.parse_xml_response(contents)

    async def aiotrack(self, tracking_number):
        url = self.url_for(tracking_number)
        async with ClientSession() as session:
            async with session.get(url) as response:
                contents = await response.read()
        return self.parse_xml_response(contents)
