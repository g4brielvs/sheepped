#!/usr/bin/env python

import json

import requests
import xmltodict
from lxml import etree


class USPSError(Exception):
    pass


class USPS:
    """
    Wrapper around USPS tracking API
    :param str user_id: USPS User ID
    """

    URL = "https://secure.shippingapis.com/ShippingAPI.dll?API=TrackV2&XML="

    def __init__(self, user_id):
        self.user_id = user_id

    def url_for(self, tracking_number):
        xml = etree.Element("TrackFieldRequest", {"USERID": self.user_id})
        etree.SubElement(xml, "TrackID", {"ID": tracking_number})
        value = etree.tostring(xml).decode()
        return f"{self.URL}{value}"

    def track(self, tracking_number):
        url = self.url_for(tracking_number)
        xml_response = requests.get(url).content
        response = json.loads(json.dumps(xmltodict.parse(xml_response)))
        if "Error" in response:
            raise USPSError(response["Error"])
        return response
