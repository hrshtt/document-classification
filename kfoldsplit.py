import pandas as pd
import fasttext
from sklearn.model_selection import StratifiedKFold


all_text_path = './data/all_text.txt'
with open(all_text_path, 'r') as f:
    data = f.read().split('\n')

df = pd.DataFrame(data = [(text.split(' ', 1)[0], ' '.join(text.split(' ')[0:300])) for text in data], columns= ['labels', 'text'])

#shuffle the data if required
# df = df.sample(frac=1).reset_index(drop=True)

kf = StratifiedKFold(n_splits=5, shuffle=True)

i=0
test_score, train_score, all_score = [], [], []
for train_index, test_index in kf.split(df['text'],df['labels']):
    train_path = './temp_train.txt'
    test_path = './temp_test.txt'
    i+=1
    X_train = df['text'][train_index]
    X_test = df['text'][test_index]
    with open(train_path, 'w') as trn:
        trn.write('\n'.join(X_train))
    with open(test_path, 'w') as tst:
        tst.write('\n'.join(X_test))
    model = fasttext.train_supervised('./temp_train.txt', ws=1, loss='ns',autotuneValidationFile='./temp_test.txt', autotuneModelSize="2M")
    test_score.append(model.test(test_path))
    train_score.append(model.test(train_path))
    all_score.append(model.test(all_text_path))
    print(f"Training Set: {train_score[i-1]}")
    print(f"Testing Set: {test_score[i-1]}")
    print(f"All Data: {all_score[i-1]}")
    
i=0
for test, train, all_ in zip(test_score, train_score, all_score):
    i += 1
    print(f'fold-{i}')
    print(f'Precision: Test: {test[1]:.4f}, Train: {train[1]:.4f}, All: {all_[1]:.4f}')
    print(f'Recall:  Test: {test[2]:.4f}, Train: {train[2]:.4f}, All: {all_[2]:.4f}')
    print(f'F1:  Test: {(2*test[1]*test[2])/(test[1] + test[2]):.4f}, Train: {2*train[1]*train[2]/(train[1] + train[2]):.4f}, All: {2*all_[1]*all_[2]/(all_[1] + all_[2]):.4f}')

