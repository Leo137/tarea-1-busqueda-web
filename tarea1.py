# @ Tarea 1 - Tecnologias de busqueda en la Web
#             Leonardo - - 
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


# Homework 1 - 
vocabulary = list()
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
			# Step 1
			#collocations = 
			#vocabulary.expand(collocations)

			# Step 2 and 3
			# Get sentences
			sentencias = get_sentencias(text_data[2])

			# Get unigrams from sentences
			unigrams = list()
			for sentencia in sentencias:
				unigrams.extend(get_tokens(sentencia))

			# Add sentences-unigrams to vocabulary
			vocabulary.extend(unigrams)

			# Step 4 - Inverted Index
			# TO-Do