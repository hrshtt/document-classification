#! /home/hrshtt/Documents/Code/NLP/Massive_Modules/bin/python
import pycaret.nlp as pycNLP
import os
from pathlib import Path
from pprint import pprint

#Path to text files
text_dir = Path('/home/hrshtt/Documents/Data/doc_class_text')

def get_all_text():
    all_text = []
    for i, folder in enumerate(os.listdir(text_dir)):
        for file_ in os.listdir(text_dir / folder):
            with open(text_dir / folder / file_) as f:
                all_text.append((folder, f.read().strip()))
    return(all_text)

if __name__ == "__main__":
    
    text_list = get_all_text()

    cleaned_text_obj = pycNLP.setup([text[1] for text in text_list])
    
    test_text = '\n'
    for label, text in zip([data[0] for data in text_list], cleaned_text_obj[0]):
        if ''.join(text).strip() != '':
            test_text += f'__label__{label} {" ".join([txt.replace("_"," ") for txt in text])}\n'
            # test_text += f'{" ".join([txt.replace("_"," ") for txt in text])}\n'

    with open('./data/processed_text.txt', 'w') as f:
        f.write(test_text.strip())