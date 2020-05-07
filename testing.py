import fasttext
from pprint import pprint

model = fasttext.load_model("./models/model_file.bin")
print(f"Training set Accuracy: {model.test('./data/train_text.txt')}")

print(f"Testing set Accuracy: {model.test('./data/test_text.txt')}")
