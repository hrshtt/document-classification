import fasttext

model = fasttext.train_supervised('./data/train_text.txt', lr=0.005, epoch=1000, wordNgrams = 3)

model.save_model("./models/model_file.bin")