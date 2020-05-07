# Uses KoiReader API to mine text from documents
import os
import requests
from pprint import pprint
from ocr_koireader_ip import koireaderAPIip as API_URL
from PyPDF2 import PdfFileReader, PdfFileWriter
from pathlib import Path


def get_ocr(filepath):

    print(os.path.join(text_path, path, filename.stem + '.txt'))

    if filepath.suffix.lower() == '.pdf':
        pdf = PdfFileReader(open(filepath, "rb"))
        if pdf.numPages > 1:
            output = PdfFileWriter()
            output.addPage(pdf.getPage(0))
            with open("temp.pdf", "wb") as outputStream:
                output.write(outputStream)
            filepath = Path("temp.pdf")

    with open(filepath, 'rb')as f:
        file_ = f.read()
        print("Sending request")
        ocr_result = requests.post(API_URL, files={"file" : file_})
        if ocr_result.status_code==200:
            print("success")
            output = []
            ocr_result = ocr_result.json()['ocr']
            if filepath.suffix.lower() == '.pdf':
                output = ocr_result
            else:
                output.append(ocr_result)
            for page in output:
                page.sort(key= lambda x: (x[0][1], x[0][0]))
                doc_text = ' '.join(i[1] for i in page)
                # print(f"doc_text : {doc_text}")
            return doc_text
        else:
            print('ocr down')
            return None

#path to the dataset
#the dataset directory format requirement: Dataset_path/ {class_name} / {corresponding files}
#in the directory only keep folders whose class is of scope

dataset_path = Path('/home/hrshtt/Documents/Data/doc_class_dataset')
text_path = Path('/home/hrshtt/Documents/Data/doc_class_text')

files_dict = {}
text_dict = {}

for root, dirs, files in os.walk(text_path):
    if files !=[]:
        text_dict[os.path.basename(root)] = [Path(file_) for file_ in files]



for root, dirs, files in os.walk(dataset_path):
    if files != []:
        # if 'XPO' in root:
        # files_dict[os.path.basename(root)] = [file_ for file_ in files if file_.endswith('.pdf')]
        files_dict[os.path.basename(root)] = [Path(file_) for file_ in files if Path(file_).stem not in [text_.stem for text_ in text_dict[os.path.basename(root)]] ]

print(len(files_dict['bol']), len(files_dict['orders']), len(files_dict['invoices']))
print(len(text_dict['bol']), len(text_dict['orders']), len(text_dict['invoices']))
#path to store text

# for path in files_dict:
#     if not os.path.exists(os.path.join(text_path,path)):
#         os.mkdir(os.path.join(text_path, path))
#     for filename in files_dict[path]:
#         # print(path, filename)
#         filepath = dataset_path / path / filename
#         print(filepath)
#         doc_text = get_ocr(filepath)
#         if doc_text !=None:
#             with open(os.path.join(text_path, path, filename.stem + '.txt'), 'w') as f:
#                 f.write(doc_text)
#                 print(os.path.join(text_path, path, filename.stem + '.txt'), ' is written to disk successfully')
#         else:
#             print(os.path.join(text_path, path, filename.stem + '.txt'), ' Unable to write file')