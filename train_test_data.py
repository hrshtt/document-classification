import re
import os
from pathlib import Path
import pandas as pd

#Path to text files
text_dir = Path('/home/hrshtt/Documents/Data/doc_class_text')

def preprocess_text(document):
        # Remove all the special characters
        document = re.sub(r'\W', ' ', str(document))

        # Give Space between adjecent chars and nums 
        document = re.sub(r"([0-9]+(\.[0-9]+)?)",r" \1 ", document)

        # Remove all single characters
        document = re.sub(r'\s+[a-zA-Z]\s+', ' ', document)

        # Remove single characters from the start
        document = re.sub(r'\^[a-zA-Z]\s+', ' ', document)

        # Replace _ with space
        document = re.sub(r'[_]', ' ', document)

        # Substituting multiple spaces with single space
        document = re.sub(r'\s+', ' ', document, flags=re.I)

        # Removing prefixed 'b'
        document = re.sub(r'^b\s+', '', document)

        # Replacing numbers with #
        document = clean_numbers(document)

        # Converting to Lowercase
        document = document.lower()

        tokens = [word for word in document.split() if len(word) > 3 and len(word) < 15]

        preprocessed_text = ' '.join(tokens)

        return preprocessed_text

def clean_numbers(x):

    x = re.sub('[0-9]', '#', x)

    return x
        
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
    
    # text_data = []
    # for class_ in all_text_list_clean:
    #     for value in all_text_list_clean[class_]:
    #         text_data.append({'class': '__label__'+ class_, 'text' : value})
    # text_df = pd.DataFrame(text_data)
    
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