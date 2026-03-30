import pandas as pd
from ofxparse import OfxParser
from apps.integrations.functions.porto_seguro_importer import PortoSeguroInvoiceImporter

class ImportFile:
    def __init__(self, file):
        self.file = file

    def excel_import(self):
        pass

    def ofx_import(self):
        pass

    def csv_import(self):
        pass

    def pdf_import(self):
        pass
        
    def porto_seguro_import(self, account_id, year):
        importer = PortoSeguroInvoiceImporter(self.file, account_id, year)
        return importer.process()