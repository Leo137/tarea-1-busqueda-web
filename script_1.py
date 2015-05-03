import os
import nltk
from pprint import pprint as pp
import script_4

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
            stop = nltk.corpus.stopwords.words("english") 
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
    
    finder = nltk.collocations.BigramCollocationFinder.from_words(text)
    finder.apply_freq_filter(3)
    return finder.nbest(bigram_measures.pmi, 10*len(os.listdir("abstracts"))) # detectar collocations
    
def get_vocabulary_from_collocations(bigrams):
    vocab = list()
    words = [(w[0] + " " + w[1]).lower() for w in bigrams]
    vocab.extend(sorted(set(words))) # agregar a vocabulario 
    return sorted(set(vocab))
    
def create_inverted_index(collocations):

    inverted_index = {}
    # Open ALL abstracts
    for file in os.listdir("abstracts"):
        if file.endswith(".txt"):
        
            # Read Text
            f = open("abstracts/" + file,"r")
            file_text = f.read()
            
            # Get tokens
            tokens = (nltk.word_tokenize(file_text))
            
            # Stopwords detection
            stop = nltk.corpus.stopwords.words("english") 
            filtered = [token.lower() for token in tokens if token not in stop]
            
            # Generate processed text
            text = nltk.Text(filtered)
            
            # Remove possible punctuation marks
            puncts = ".,?!:;{}[]()<>$'"
            for sym in puncts:
                text  = [item for item in text if item != sym]
            
            # Get bigrams
            b = nltk.bigrams(text)
            
            # Find matches and add them to the inverted index
            for match in (set(collocations) & set(b)):
                value = match[0] + " " + match[1]
                if value in inverted_index:
                    inverted_index[value].append(file)
                else:
                    inverted_index[value] = [file]
    
    return inverted_index
    
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
    
    script_4.script_4(bigrams)

script_1()