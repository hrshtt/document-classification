import os
from pathlib import Path
from preprocessing import preprocess_text

#Path to text files
text_dir = Path('/home/hrshtt/Documents/Data/doc_class_text')


def get_all_text():
    all_text = {}
    for folder in os.listdir(text_dir):
        all_text[folder] = []
        for file_ in os.listdir(text_dir / folder):
            with open(text_dir / folder / file_) as f:
                all_text[folder].append(f.read().strip())
    return(all_text)

if __name__ == "__main__":
    
    #reading files and getting the data as a dict
    all_text_list = get_all_text()

    #cleaning and preprocessing the data
    all_text_list_clean = {}
    for i, class_ in enumerate(all_text_list):
        all_text_list_clean[class_] = []
        for j, _ in enumerate(all_text_list[class_]):
            all_text_list_clean[class_].append(preprocess_text(all_text_list[class_][j]))
    
    #first 45 documents of each class as train set
    train_text = ''
    for i, class_ in enumerate(all_text_list_clean):
            for value in all_text_list_clean[class_][0:45]:
                if value.strip()!= '':
                    train_text += f'__label__{i} {value}\n'
    with open('./data/train_text.txt', 'w') as f:
        f.write(train_text.strip())

    #rest of the documents of each class as test set
    test_text = '\n'
    for i, class_ in enumerate(all_text_list_clean):
            for value in all_text_list_clean[class_][45:]:
                if value.strip()!= '':
                    test_text += f'__label__{i} {value}\n'
    with open('./data/test_text.txt', 'w') as f:
        f.write(test_text.strip())