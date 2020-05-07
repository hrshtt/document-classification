from pathlib import Path
import os
from pprint import pprint

def get_word(text, head, middle, tail):
    label = text.split(' ', 1)[0]
    text = text.split(' ', 1)[1].split(' ')
    mid = len(text)//2
    return ' '.join([label, ' '.join(text[0:head]), ' '.join(text[mid-middle:mid+middle]), ' '.join(text[len(text)-tail:])])
    
def get_all_text():
    with open('./data/all_text.txt', 'r') as f:
        all_text = f.read().split('\n')
    all_text.sort()
    return all_text

def save_file(head, middle, tail):
    text_list = get_all_text()
    for i, text in enumerate(text_list):
        text_list[i] = get_word(text, head, middle, tail)

    file_name = os.path.join('./data/subsets',f'subset_{head}-{middle}-{tail}.txt')
    
    with open(os.path.join(file_name), 'w') as f:
        f.write('\n'.join(text_list))
    print(f'New subset created: {file_name}')


if __name__ == "__main__":
    
    print('Splitting Each document with for Given word ranges: ')
    print(75*'-')
    print(f'Enter the number of words you want from each place in a Document: ')
    print(75*'-')
    print('Enter 0 if none')
    head = int(input('Head: '))
    middle = int(input(f'Middle (+/- n words from center): '))
    tail = int(input('Tail: '))
    save_file(head, middle, tail)