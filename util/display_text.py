#Prints text of all text files from given folder
import os
from pathlib import Path
from pprint import pprint

text_dir = Path('/home/hrshtt/Documents/Data/scrapped_data/text')

all_text_files = []
for root, dirs, files in os.walk(text_dir):
    if files != []:
        for filepath in files:
            if filepath.endswith('.txt'):
                if dirs != []:
                    all_text_files.append(os.path.join(root, dirs, filepath))
                else:
                    all_text_files.append(os.path.join(root, filepath))

pprint(all_text_files)

for filepath in all_text_files:
    if input('Enter any character to continue:'):
        print(f'{filepath}\n')
        with open(filepath) as f:
            print(f.read().strip()) 
    print()