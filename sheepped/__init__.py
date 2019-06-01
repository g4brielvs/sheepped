#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import xmltodict

from lxml import etree

class USPS(object):
    '''
    Wrapper around USPS tracking API

    :param str user_id: USPS User ID
    '''
    def __init__(self, user_id):
        self.user_id = user_id

    API_URL = 'https://secure.shippingapis.com/ShippingAPI.dll?API='

    def track(self, tracking_number):
        xml = etree.Element('TrackFieldRequest', {'USERID': self.user_id})
        child = etree.SubElement(xml, 'TrackID', {'ID': tracking_number})

        xml = etree.tostring(xml).decode()
        url = f'{self.API_URL}TrackV2&XML={xml}'

        xml_response = requests.get(url).content
        response = json.loads(json.dumps(xmltodict.parse(xml_response)))
        if 'Error' in response:
            raise
        return response
