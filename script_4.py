import os
import nltk
import script_2

def create_inverted_index(collocations):

    inverted_index = {}
    # Open ALL abstracts
    for file in os.listdir("abstracts"):
        if file.endswith(".txt"):
        
            # Read Text
            f = open("abstracts/" + file,"r")
            file_text = f.read()
            
            # Get sentences
            sentences = script_2.get_sentencias(file_text)
            
            unigrams = list()
            # Get unigrams based on tokens
            for sentence in sentences:
                unigrams.extend(script_2.get_tokens(sentence))
            
            # Get bigrams
            bigrams = [item[0] + " " + item[1] for item in nltk.bigrams(unigrams)]
            
            t = unigrams + bigrams
            
            # Find matches and add them to the inverted index
            for match in (set(collocations) & set(t)):
                value = match
                if value in inverted_index:
                    inverted_index[value].append(file)
                else:
                    inverted_index[value] = [file]
    
    return inverted_index
    
def script_4(vocab):

    # Get the inverted index
    inverted_index = create_inverted_index(vocab)
    
    # Write to file
    i = open("inverted.txt","w")
    for k,v in sorted(inverted_index.items(),key=lambda tuple: tuple[0]):
        i.write("'" + k + "' : [")
        for item in v:
            i.write("'" + item + "' ")
        i.write("]\n")
    i.close()
    
    print("$ {0} keys founded, saved inverted index to inverted.txt".format(len(inverted_index)))