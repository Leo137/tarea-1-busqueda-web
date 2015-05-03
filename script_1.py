import os
import nltk
from nltk.corpus import stopwords

vocab = list()
for file in os.listdir("abstracts"):
    if file.endswith(".txt"):
        f = open("abstracts/" + file,"r")
        file_text = f.read()
        tokens = nltk.word_tokenize(file_text)
        text = nltk.Text(tokens)
        # collocations = text.collocations() # detectar collocations
        words = [w.lower() for w in text]
        vocab.extend(sorted(set(words))) # agregar a vocabulario 
puncts = ".,?!:;{}[]()<>"
for sym in puncts:
    vocab = [item for item in vocab if item != sym]
vocab = sorted(set(vocab))
v = open("vocab.txt","w")
for element in vocab:
    v.write("'" + element + "'" + ",")
v.close()