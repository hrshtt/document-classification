import fasttext

model = fasttext.train_supervised('./data/train_text.txt')

model.save_model("./models/model_file.bin")