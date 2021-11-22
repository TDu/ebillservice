import os
import requests
import zeep

SSL_CERTIF = os.path.join(os.path.dirname(__file__), "certificates", "ebill-ki.postfinance.ch.cer")
WSDL_DOC = os.path.join(os.path.dirname(__file__), "certificates", "ebill-ki.postfinance.ch.cer")


class Paynet:
    def __init__(self):
        self.use_test_service = True
        settings = zeep.Settings(xml_huge_tree=True)
        session = requests.Session()
        session.verify = SSL_CERTIF
        transport = zeep.transports.Transport(session=session)
        self.client = zeep.Client(WSDL_DOC, transport=transport, settings=settings)

    def ping(self):
        print("Ping")
