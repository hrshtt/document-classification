import fasttext

model = fasttext.train_supervised('./data/train_text.txt', lr=0.009, epoch=10000, minCount= 2, wordNgrams = 3)

model.save_model("./models/model_file.bin")