import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os
with open('./data/train_text.txt') as f:
    all_sizes = [len(text) for text in f.read().split('\n')]

print(sum(all_sizes)/len(all_sizes))

plt.xlim([min(all_sizes)-5, max(all_sizes)+5])

plt.hist(all_sizes, bins=15, alpha=0.5)

plt.xlabel('length of the document')
plt.ylabel('count')

plt.show()


text_dir = Path('/home/hrshtt/Documents/Data/doc_class_text')

def get_train_all_text():
    all_text = []
    for i, folder in enumerate(os.listdir(text_dir)):
        for file_ in os.listdir(text_dir / folder)[0:45]:
            with open(text_dir / folder / file_) as f:
                all_text.append((folder, f.read().strip()))
    return(all_text)