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
    
    #saving text as minimal processed doc
    all_text = ''
    for class_ in all_text_list_clean:
            for value in all_text_list_clean[class_]:
                if value.strip()!= '':
                    all_text += f'__label__{class_} {value}\n'
                    # all_text += f'{value}\n'

    with open('./data/raw_text.txt', 'w') as f:
        f.write(all_text.strip())

