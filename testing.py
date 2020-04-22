import fasttext
from pprint import pprint

model = fasttext.load_model("./models/model_file.bin")
print(model.test('./data/test_text.txt'))

# results = []
# groundtruths = []
# with open('./data/test_text.txt', 'r') as f:
#     for line in f.read().split('\n'):
#         results.append((model.predict(line, k=1)[0][0]))
#         groundtruths.append(line.split(' ',1)[0])

# correct = 0
# for pred, truth in zip(results, groundtruths):
#     if pred == truth:
#         correct += 1
#     print(pred, truth)
# print(f'{correct/len(groundtruths)}')