# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import os
import requests
import zeep

SSL_CERTIF = os.path.join(os.path.dirname(__file__), "certificates", "SwissSign_Gold_CA-G2.cer")
WSDL_DOC = os.path.join(os.path.dirname(__file__), "wsdl", "b2bservice.wsdl")


class Paynet:
    def __init__(self, url, test_service):
        self.use_test_service = True
        settings = zeep.Settings(xml_huge_tree=True)
        session = requests.Session()
        session.verify = SSL_CERTIF
        transport = zeep.transports.Transport(session=session)
        self.client = zeep.Client(WSDL_DOC, transport=transport, settings=settings)
        self.service = self.client.create_service("{http://ch.swisspost.ebill.b2bservice}UserNamePassword", url)

    def ping(self):
        print("Call ExecutePing method")
        self.service.ExecutePing("yellow", None, False, False)
