import os
import nltk
from nltk.corpus import stopwords
from nltk.collocations import *
vocab = list()
bigram_measures = nltk.collocations.BigramAssocMeasures()
text = list()

for file in os.listdir("abstracts"):
    if file.endswith(".txt"):
        f = open("abstracts/" + file,"r")
        file_text = f.read()
        tokens = (nltk.word_tokenize(file_text))
        
        stop = stopwords.words("english") # deteccion stopwords
        filtered = [token.lower() for token in tokens if token not in stop]
        text.extend(nltk.Text(filtered))
        
puncts = ".,?!:;{}[]()<>$'"
for sym in puncts:
    text  = [item for item in text if item != sym]
finder = BigramCollocationFinder.from_words(text)
finder.apply_freq_filter(3)
bigrams = finder.nbest(bigram_measures.pmi, 10*len(os.listdir("abstracts"))) # detectar collocations
words = [(w[0] + " " + w[1]).lower() for w in bigrams]
vocab.extend(sorted(set(words))) # agregar a vocabulario 

vocab = sorted(set(vocab))
v = open("vocab.txt","w")
for element in vocab:
    v.write("'" + element + "'" + ",")
v.close()