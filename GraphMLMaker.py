
import os
import sys
import re
from nltk import word_tokenize
from string import punctuation
from nltk.util import ngrams
from collections import Counter
import networkx as nx
import numpy as np
import pickle

"""provide the name of the folder with the texts, and the name of the folder where to put graphs"""


punct = punctuation + "«»—…“”*№–"

current_path = os.getcwd()
start_path = current_path + "/" + sys.argv[1]
output_path = current_path + "/" + sys.argv[2]
files = []


for start, dirs, f in os.walk(start_path):
	for fname in f:
		if not fname.startswith('.'):
			files.append(fname)
           



def read_file(file_name):
	with open(file_name, "r") as f:
		return f.read()





def make_sentences(txt):
    delim = [char for char in "!.?…"]
    pattern = "|".join(map(re.escape, delim))
    sents_list = [sent.strip() for sent in re.split(pattern, txt)]
    sentences = [sent for sent in sents_list if sent]
    return sentences


def tokenize_sentences(sentences):
    sents_tokenized = [word_tokenize(sentence.lower()) for sentence in sentences]
    sentences_tokenized = []
    for sent in sents_tokenized:
        words = []
        for word in sent:
            if not all([char in punct for char in word]):
                words.append(word)
        sentences_tokenized.append(words)
    return sentences_tokenized


def make_bigrams(tokenized_sentences):
    bigrams = []
    for sent in tokenized_sentences:
        bi = list(ngrams(sent, 2))
        bigrams.extend(bi)
    return bigrams 


def make_graph(bigrams):
    count = Counter(bigrams).most_common()
    net = nx.DiGraph()
    for x in count:
        net.add_edge(x[0][0], x[0][1], weight=x[1])
    return net





def write_net_to_graphml(network, fname):
    file = output_path + "/" + fname[:-4] + ".graphml"
    nx.write_graphml(network, file)

        




def main(file_list):
    failed_files = []
    for fname in file_list:
        try:
            print(fname)
            file_name = start_path + "/" + fname
            text = read_file(file_name)
            sents = make_sentences(text)
            tokenized_sents = tokenize_sentences(sents)
            bigrams = make_bigrams(tokenized_sents)
            network = make_graph(bigrams)
            write_net_to_graphml(network, fname)
        except UnicodeDecodeError:
            failed_files.append(fname)
            continue
    if failed_files:
        print("Failed files:")
        for f in failed_files:
            print(f)
    return 





main(files)















	