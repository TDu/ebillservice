# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import os
import requests
import zeep
from zeep.wsse.username import UsernameToken

SSL_CERTIF = os.path.join(os.path.dirname(__file__), "certificates", "SwissSign_Gold_CA-G2.cer")
WSDL_DOC = os.path.join(os.path.dirname(__file__), "wsdl", "b2bservice.wsdl")


class EbillService:
    def __init__(self, url, test_service, username, password):
        self.use_test_service = True
        settings = zeep.Settings(xml_huge_tree=True)
        session = requests.Session()
        session.verify = SSL_CERTIF
        transport = zeep.transports.Transport(session=session)
        self.client = zeep.Client(WSDL_DOC, transport=transport, settings=settings, wsse=UsernameToken(username, password))
        self.service = self.client.create_service("{http://ch.swisspost.ebill.b2bservice}UserNamePassword", url)

    def ping(self):
        self.service.ExecutePing(
            BillerID="yellow",
            eBillAccountID=None,
            ErrorTest=False,
            ExceptionTest=False
        )
