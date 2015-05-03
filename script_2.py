import os
import nltk


def split_text_data(data):
	separator = ";;;"
	try:
		return data.split(separator)
	except:
		return None
		
def get_sentencias(texto):
	sentencias = list()
	sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	return sent_tokenizer.tokenize(texto) 

def process_sentencia(sentencia):
	

def test():
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
				# Get sentences
				sentences = get_sentencias(text_data[2])
				print(sentences)

				# Count books
				processed += 1
			else:
				corrupted += 1

	print("$ {0} Abstracts processed. {1} corrupted.".format(processed, corrupted))

test()