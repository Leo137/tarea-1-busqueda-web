import os
import nltk

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
    
def script_4(bigrams):

    # Get the inverted index
    inverted_index = create_inverted_index(bigrams)
    
    # Write to file
    i = open("inverted.txt","w")
    for k,v in inverted_index.items():
        i.write("'" + k + "' : [")
        for item in v:
            i.write("'" + item + "' ")
        i.write("]\n")
    i.close()
    
    print("$ {0} keys founded, saved inverted index to inverted.txt".format(len(inverted_index)))