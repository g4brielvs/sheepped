#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import xmltodict

from lxml import etree

class USPSApiError(Exception):
    pass


class USPSApi(object):
    BASE_URL = 'https://secure.shippingapis.com/ShippingAPI.dll?API='
    urls = {
        'tracking': 'TrackV2{test}&XML={xml}',
        'label': 'eVS{test}&XML={xml}',
        'validate': 'Verify&XML={xml}',
    }

    def __init__(self,  api_user_id, test=False):
        self.api_user_id = api_user_id
        self.test = test

    def get_url(self, action, xml):
        return self.BASE_URL + self.urls[action].format(
            **{'test': 'Certify' if self.test else '', 'xml': xml}
        )

    def send_request(self, action, xml):
        xml = etree.tostring(xml, pretty_print=self.test).decode()
        url = self.get_url(action, xml)
        xml_response = requests.get(url).content
        response = json.loads(json.dumps(xmltodict.parse(xml_response)))
        if 'Error' in response:
            raise USPSApiError(response['Error']['Description'])
        return response


    def track(self, *args, **kwargs):
        return TrackingInfo(self, *args, **kwargs)


class TrackingInfo(object):

    def __init__(self, usps, tracking_number):
        xml = etree.Element('TrackFieldRequest', {'USERID': usps.api_user_id})
        child = etree.SubElement(xml, 'TrackID', {'ID': tracking_number})

        self.result = usps.send_request('tracking', xml)