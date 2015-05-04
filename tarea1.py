# @ Tarea 1 - Tecnologias de busqueda en la Web
#             Leonardo Santis - 2010735478 - leonardo.santis@alumnos.usm.cl
#             Miguel Diaz - 27030297 - miguel.diaz@mdiazlira.com

import os
import nltk
from nltk.corpus import stopwords
from pprint import pprint as pp

# This method is usted to split the title, author and abstract from a series of
# well-formed-texts. A Well-formed-texts follows the following structure:
#   title;;;author;;;abstract
#
# Return 3-tuple -> (title, author, abstract)
def split_text_data(data):
    separator = ";;;"
    try:
        return data.split(separator)
    except:
        return None

# This method is used to get Sentences from a particular text
#
# Return: Sentences found on text
def get_sentencias(texto):
    sentencias = list()
    sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    return sent_tokenizer.tokenize(texto) 

# This method is used to get Tokens from a particular sentence
# The process is as follows:
#   1.- Lowercase everything
#   2.- Remove Punctuations and Some Latex Symbols
#   3.- Remove Stopwords from English dictionary (NLTK)
#   4.- Lemmatize tokens found on sentences
#
# Return: List of unigrams from sentence.
def get_tokens(sentencia):
    # To Lower
    sentencia = sentencia.lower()

    # Remove Punctuation and Latex Stuff
    puncts = ",;.$\\\\"
    for sym in puncts:
        sentencia = sentencia.replace(sym," ")

    # Tokenize
    sentencia.strip()
    tokens = nltk.word_tokenize(sentencia)

    # Removing Stopwords and latex stuff
    stop = stopwords.words("english")
    stop_latex = ["$","\\"]
    stop.extend(stop_latex)
    tokens = [token.lower() for token in tokens if token not in stop]

    # Wordnet Lematization
    wnl = nltk.WordNetLemmatizer()
    tokens = [wnl.lemmatize(token) for token in tokens]

    return tokens
    
def get_collocations(texto):
    # Bigram measures
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    
    finder = nltk.collocations.BigramCollocationFinder.from_words(texto)
    finder.apply_freq_filter(3)
    # Detectar collocations
    bigrams = finder.nbest(bigram_measures.pmi, 10*len(os.listdir("abstracts")))
    
    collocations = list()
    words = [(w[0] + " " + w[1]).lower() for w in bigrams]
    collocations.extend(sorted(set(words))) # agregar a vocabulario 
    return sorted(set(collocations))
    
def create_inverted_index(collocations,files,mode):
    inverted_index = {}
    for file in files:
            sentences = file[mode]
            # Get unigrams and tokens
            unigrams = list()
            for sentence in sentences:
                unigrams.extend(get_tokens(sentence))
                
            # Generate processed text
            text = nltk.Text(unigrams)
            # Get bigrams
            bigrams = [item[0] + " " + item[1] for item in nltk.bigrams(unigrams)]
            
            t = unigrams + bigrams
            
            # Find matches and add them to the inverted index
            for match in (set(collocations) & set(t)):
                value = match
                if value in inverted_index:
                    inverted_index[value].append(file[0])
                else:
                    inverted_index[value] = [file[0]]
    
    return inverted_index


# Homework 1 - 
vocabulary = list()
files = list()
# Open ALL abstracts
for file in os.listdir("abstracts"):
    if file.endswith(".txt"):
        # Read Text
        f = open("abstracts/" + file,"r")
        file_text = f.read()

        # Split data text
        text_data = split_text_data(file_text)

        # If data is correct (well-formed-texts)
        if len(text_data) == 3:
            # Step 2 and 3
            # Get sentences
            sentencias_titulo = get_sentencias(text_data[0])
            sentencias_texto = get_sentencias(text_data[2])
            
            # Get unigrams from sentences
            unigrams = list()
            for sentencia in (sentencias_titulo + sentencias_texto):
                unigrams.extend(get_tokens(sentencia))
                
            # Add sentences-unigrams to vocabulary
            vocabulary.extend(unigrams)
            
            # Step 1
            # Get collocations
            collocations = get_collocations(nltk.Text(unigrams))
            
            # Add document-collocations to vocabulary
            vocabulary.extend(collocations)

            # Add file to list of files with their sentences
            files.append([file,sentencias_titulo,sentencias_texto])
# Step 4
# Get inverted indexes
inverted_index_title = create_inverted_index(vocabulary,files,1)
inverted_index_text = create_inverted_index(vocabulary,files,2)
            
# Order vocabulary
vocabulary = sorted(set(vocabulary))

# Write vocabulary to file
v = open("vocabulary.txt","w")
for element in vocabulary:
    v.write("'" + element + "'" + ",")
v.close()

# Write the inverted index of titles to file
i = open("inverted_title.txt","w")
for k,v in sorted(inverted_index_title.items(),key=lambda tuple: tuple[0]):
    i.write("'" + k + "' : [")
    for item in v:
        i.write("'" + item + "' ")
    i.write("]\n")
i.close()

# Write the inverted index of texts to file
i = open("inverted_text.txt","w")
for k,v in sorted(inverted_index_text.items(),key=lambda tuple: tuple[0]):
    i.write("'" + k + "' : [")
    for item in v:
        i.write("'" + item + "' ")
    i.write("]\n")
i.close()

print("$ {0} keys founded, saved inverted index to inverted_title.txt".format(len(inverted_index_title)))
print("$ {0} keys founded, saved inverted index to inverted_text.txt".format(len(inverted_index_text)))
print("$ {0} Vocabulary items founded, saved in vocabulary.txt".format(len(vocabulary)))