
import os
import sys
import re
from nltk import sent_tokenize, word_tokenize

"""provide the name of the folder with the texts and the name of the language"""


current_path = os.getcwd()
start_path = current_path + "/" + sys.argv[1]
language_name = sys.argv[2]
#output_path = current_path + "/" + sys.argv[2]
files = []


for start, dirs, f in os.walk(start_path):
	for fname in f:
		if not fname.startswith('.'):
			files.append(fname)
           



def read_file(file_name):
	with open(file_name, "r") as f:
		return f.read()



def make_sentences(text):
    sents_list = sent_tokenize(text)
    sentences = [sent for sent in sents_list if (len(word_tokenize(sent)) > 1) and (len(word_tokenize(sent)) <= 200)]
    return sentences


def remove_newlines(sentences):
    clean_sents = []
    for sent in sentences:
        new_sent = re.sub("\n", " ", sent)
        clean_sents.append(new_sent)
    return clean_sents



#with open("Networks/texts/tryfile.txt", "w") as f:
 #   f.write("\n".join(new_tokens))

def write_sents_to_file(sentences):
    file = start_path + "/" + language_name + "_megafile.txt"
    with open(file, "w") as f:
        f.write("\n".join(sentences))

        




def main(file_list):
    failed_files = []
    list_of_sents = []
    for fname in file_list:
        try:
            print(fname)
            file_name = start_path + "/" + fname
            text = read_file(file_name)
            sents = make_sentences(text)
            list_of_sents.extend(sents)
        except UnicodeDecodeError:
            failed_files.append(fname)
            continue

    clean_sents = remove_newlines(list_of_sents)

    write_sents_to_file(clean_sents)


    if failed_files:
        print("Failed files:")
        for f in failed_files:
            print(f)

    print("The {} megafile has {} sentences".format(language_name, len(clean_sents)))
    return 





main(files)















	