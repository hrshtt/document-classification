# Uses KoiReader API to mine text from documents
import os
import requests
from pprint import pprint
from ocr_koireader_ip import koireaderAPIip as API_URL

files_dict = {}

#path to the dataset
#the dataset directory format requirement: Dataset_path/ {class_name} / {corresponding files}
#in the directory only keep folders whose class is of scope

dataset_path = '/home/hrshtt/Documents/Data/doc_class_dataset'

for root, dirs, files in os.walk(dataset_path):
    if files != []:
        files_dict[os.path.basename(root)] = files

#path to store text
text_path = '/home/hrshtt/Documents/Data/doc_class_text'

for path in files_dict.keys():
    if not os.path.exists(os.path.join(text_path, path)):
        os.mkdir(os.path.join(text_path, path))
    for filename in files_dict[path]:
        # print(path, filename)
        filepath = os.path.join(dataset_path, path, filename)
        print(os.path.join(text_path, path, filename.split('.')[0] + '.txt'))
        with open(filepath, 'rb')as f:
            file_ = f.read()
            print("Sending request")
            ocr_result = requests.post(API_URL, files={"file" : file_})
            if ocr_result.status_code==200:
                print("success")
                output = []
                ocr_result = ocr_result.json()['ocr']
                if filepath.lower().endswith('.pdf'):
                    output = ocr_result
                else:
                    output.append(ocr_result)
                for page in output:
                    page.sort(key= lambda x: (x[0][1], x[0][0]))
                    doc_text = ' '.join(i[1] for i in page)
                    # print(f"doc_text : {doc_text}")
                    with open(os.path.join(text_path, path, filename.split('.')[0] + '.txt'), 'w') as f:
                        f.write(doc_text)
                        print(os.path.join(text_path, path, filename.split('.')[0] + '.txt'), ' is written to disk successfully')
            else:
                print('ocr down')
    print()
