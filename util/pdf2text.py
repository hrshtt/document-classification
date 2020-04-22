import os
from pathlib import Path

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    
    try:
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)
    except TypeError:
        fp.close()
        device.close()
        retstr.close()
        return 'error'
    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

bol_extra = Path('/home/hrshtt/Documents/Data/bol_extra')
bol_list = os.listdir(bol_extra)

for bol in bol_list:
    bol_path = bol_extra / bol
    text = convert_pdf_to_txt(bol_path)
    if text != 'error':
        with open(os.path.join('/home/hrshtt/Documents/Data/doc_class_text/bol', bol_path.stem.replace(' ', '_')) + '.txt', 'w') as f :
            f.write(text.strip())
        print(f'Successfully written: {(bol_extra / bol).stem}')
    if text == 'error':
        print(f'Error writing: {(bol_extra / bol).stem}')
