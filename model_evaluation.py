import sklearn.metrics as mets
from sklearn.model_selection import train_test_split
from pathlib import Path
import pandas as pd 
import fasttext

def eval_model(model):
    files = ['./temp_test.txt','./temp_train.txt','./all_text.txt']

    for file_name in files:
        file_name = Path(file_name)
        with open(file_name , 'r') as f:
            text = f.read().split('\n')
        text.sort()

        true_labels = [txt.split(' ',1)[0] for txt in text]
        text = [txt.split(' ',1)[1] for txt in text]
        pred_labels = [label[0] for label in model.predict(text)[0]]
        print(f'Confusion Matrix for {file_name.stem}:\n{mets.confusion_matrix(y_pred=pred_labels, y_true=true_labels)}')

        print(f"F1 Score for {file_name.stem}: {mets.f1_score(true_labels, pred_labels, average='weighted'):0.4f}")
        print('---'*10)

file_name = Path(input('Enter the path to the Model'))
if not file_name.exists():
    print('The file does not exist')
    exit()
elif '.bin' != file_name.suffix:
    print('The file is not a .bin')
    exit()
else:
    eval_model(fasttext.load_model(file_name))

with open('./all_text.txt', 'r') as f:
    data = f.read().split('\n')

head = 300
tail = 50

df = pd.DataFrame(data = [(text.split(' ', 1)[0], ' '.join(text.split(' ')[0:head]+text.split(' ')[-tail:])) for text in data], columns= ['labels', 'text'])
df = df.sample(frac=1).reset_index(drop=True)

X_train, X_test, y_train, y_test = train_test_split(df['text'], df['labels'],test_size=0.33, random_state=42)

with open('./temp_train.txt', 'w') as trn:
    trn.write('\n'.join(X_train))
with open('./temp_test.txt', 'w') as tst:
    tst.write('\n'.join(X_test))

# per word level n grams (n = 2 [gr, ra, am, ms])
wordNgrams = 3
# ns loss gives best result so far, defailt is softmax
loss = 'ns'
# word level window size default is 5
ws=0

model = fasttext.train_supervised('./temp_train.txt', ws=ws, loss=loss, wordNgrams = wordNgrams, autotuneValidationFile='./temp_test.txt', autotuneModelSize="1M")

eval_model(model)
