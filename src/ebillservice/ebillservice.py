# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import base64
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
            BillerID=None,
            # BillerID="41100000158290172",
            eBillAccountID="41100000158290172",
            # eBillAccountID=None,
            ErrorTest=False,
            ExceptionTest=False
        )

    def get_invoice_data(self):
        with open(os.path.join(os.path.dirname(__file__), "invoice.xml"), "r") as f:
            data = f.read()
        return base64.b64encode(data.encode("utf-8"))

    def upload_files(self):
        data = self.get_invoice_data()
        invoice_type = self.client.get_type("ns2:Invoice")
        array_invoice_type = self.client.get_type("ns2:ArrayOfInvoice")
        invoice = invoice_type(FileType="EAI.XML", TransactionID="A00002", Data=data)
        invoices = array_invoice_type(invoice)
        res = self.service.UploadFilesReport(
            BillerID="41101000001021209",
            invoices=invoices
        )
        print(res)

    def search_invoices(self):
        parameter_type = self.client.get_type("ns2:SearchInvoiceParameter")
        parameters = parameter_type(BillerID="41101000001021209", TransactionID="A00002")
        res = self.service.SearchInvoices(
            Parameter=parameters
        )
        print(res)

    def get_invoice_list(self):
        res = self.service.GetInvoiceListBiller(
            BillerID="41101000001021209",
            ArchiveData=True,
        )
        print(res)
