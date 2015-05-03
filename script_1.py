import os
for file in os.listdir("abstracts"):
    if file.endswith(".txt"):
        f = open("abstracts/" + file,"r")
        file_text = f.read()
        # print(file_text)
        print(file)