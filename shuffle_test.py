'''
    Takes a subset of words of the Documents defined in terms of Head, Middle and Tail
    Writes result to stats.csv
'''
import os
import random
from pprint import pprint
import fasttext
from data_subset import save_file
from datetime import datetime
sub_path = './data/subsets/'

print('Give the subset details you want to test: ')
print(75*'-')
print(f'Enter the number of words you want from each place in a Document: ')
print(75*'-')
print('Enter 0 if none')
head = int(input('Head: '))
middle = int(input(f'Middle (+/- n words from center): '))
tail = int(input('Tail: '))

print(50*'--')

file_name = f'subset_{head}-{middle}-{tail}.txt'

if not os.path.exists(os.path.join(sub_path, file_name)):
    if input('Do you want to create the defined subset?[Y/N]: ').lower() == 'y':
        save_file(head, middle, tail)
        print(50*'--')

    else:
        exit()

with open(os.path.join(sub_path, file_name)) as f:
    subset_list = f.read().split('\n')

n = int(input(f'Give number of times you want to shuffle, train and test {file_name}: '))

acc_train = []
acc_test = []

f1_train = []
f1_test = []


for i in range(n):
    print(f'Run {i+1}')
    labels = set([text.split(' ',1)[0] for text in subset_list])
    newdict = {}
    for label in labels:
        newdict[label] = []
        for text in subset_list:
            if label in text:
                newdict[label].append(text)
        random.shuffle(newdict[label])

    with open('./train_temp.txt', 'w') as f:
        for label in newdict:
            f.write('\n'.join(newdict[label][0:45]))

    with open('./test_temp.txt', 'w') as f:
        for label in newdict:
            f.write('\n'.join(newdict[label][45:]))

    model = fasttext.train_supervised('./train_temp.txt', lr=0.0001, epoch=7500)
    
    result_train = model.test("./train_temp.txt")

    result_test = model.test("./test_temp.txt")

    acc_test.append(result_test[1])
    f1_test.append(result_test[2])

    acc_train.append(result_train[1])
    f1_train.append(result_train[2])


    print(f'Training Accuracy: {result_train}')

    print(f'Testing Accuracy: {result_test}')

    print(50*'--')

print(f'Average Training Set Accuracy for {file_name}: {sum(acc_train)/n}')
print(f'Average Training Set F1_Score for {file_name}: {sum(f1_train)/n}')
print(35*'--')
print(f'Average Testing Set Accuracy for {file_name}: {sum(acc_test)/n}')
print(f'Average Testing Set F1_Score for {file_name}: {sum(f1_test)/n}')

datetime_stamp = datetime.now()
with open('./stats.csv', 'a') as f:
    f.write(f'\n{datetime_stamp.ctime()}, {file_name}, {sum(acc_train)/n:.4f}, {sum(acc_test)/n:.4f}, {sum(f1_train)/n:.4f}, {sum(f1_test)/n:.4f}, {n}')