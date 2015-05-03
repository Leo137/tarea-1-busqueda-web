import os
import nltk
from nltk.corpus import stopwords
from nltk.collocations import *

def get_processed_text():
    text = list()
    
    # Open ALL abstracts
    for file in os.listdir("abstracts"):
        if file.endswith(".txt"):
        
            # Read Text
            f = open("abstracts/" + file,"r")
            file_text = f.read()
            
            # Get tokens
            tokens = (nltk.word_tokenize(file_text))
            
            # Stopwords detection
            stop = stopwords.words("english") 
            filtered = [token.lower() for token in tokens if token not in stop]
            
            # Add to processed text list
            text.extend(nltk.Text(filtered))
    
    # Remove possible punctuation marks
    puncts = ".,?!:;{}[]()<>$'"
    for sym in puncts:
        text  = [item for item in text if item != sym]
    return text
    
def find_bigrams(text):
    # Bigram measures
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    
    finder = BigramCollocationFinder.from_words(text)
    finder.apply_freq_filter(3)
    return finder.nbest(bigram_measures.pmi, 10*len(os.listdir("abstracts"))) # detectar collocations
    
def get_vocabulary_from_collocations(bigrams):
    vocab = list()
    words = [(w[0] + " " + w[1]).lower() for w in bigrams]
    vocab.extend(sorted(set(words))) # agregar a vocabulario 
    return sorted(set(vocab))
    
def script_1():

    # Procesed text list
    text = get_processed_text()
    
    # Get bigrams
    bigrams = find_bigrams(text)
    
    # Bigram collocations vocabulary list
    vocab = get_vocabulary_from_collocations(bigrams)
    
    # Write to file
    v = open("vocab.txt","w")
    for element in vocab:
        v.write("'" + element + "'" + ",")
    v.close()
    
    print("$ {0} Collocations founded, saved in vocab.txt".format(len(bigrams)))

script_1()