import os
import nltk
from nltk.corpus import stopwords

# This method is usted to split the title, author and abstract from a series of
# well-formed-texts. A Well-formed-texts follows the following structure:
#	title;;;author;;;abstract
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
#	1.- Lowercase everything
#	2.- Remove Punctuations and Some Latex Symbols
#	3.- Remove Stopwords from English dictionary (NLTK)
#	4.- Lemmatize tokens found on sentences
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


# Script to test the methods...
def script_2():
	# Abstract analized list
	abstract_list = list() 
	processed = 0
	corrupted = 0
	# Open ALL abstracts
	for file in os.listdir("abstracts"):
		if file.endswith(".txt"):

			# Read Text
			f = open("abstracts/" + file,"r")
			file_text = f.read()
			
			# Get text data (title, author, abstract)
			text_data = split_text_data(file_text)

			# If data is correct (well-formed-texts)
			if len(text_data) == 3:
				# Debug Texts
				#print "Processing: {0}".format(file)
				#print "-------------------"

				# Get sentences
				sentences = get_sentencias(text_data[2])
				
				# Debug Sentences
				#for s in sentences:
				#	print "* {0}".format(s)

				# Get unigramas based on tokens
				for sentence in sentences:
					unigramas = get_tokens(sentence)

				# Count books
				processed += 1
			else:
				corrupted += 1

	print("$ {0} Abstracts processed. {1} corrupted.".format(processed, corrupted))

script_2()