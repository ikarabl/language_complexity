
import os
import sys
import re
from nltk import word_tokenize
from string import punctuation
from nltk.util import ngrams
from collections import Counter
import networkx as nx
import numpy as np

"""
sys.argv[1] is the name of the directory with the texts
sys.argv[2] is the name of the directory where the graphs will be put
sys.argv[3] is the number of sentences per graph 
optional sys.argv[4] is the maximum number of graphs that will be made from each text file

"""
number_of_sentences_per_graph = int(sys.argv[3])

if len(sys.argv) == 5:
    max_number_of_graphs_per_language = int(sys.argv[4])
    print(f"Maximum {max_number_of_graphs_per_language} graphs will be made per language")
else:
    max_number_of_graphs_per_language = 1000000
    print("I will keep making graphs as long as I have text")








punct = punctuation + " «»—…“”*№–。！？․։՜።|፧፨፡՝\n"

current_path = os.getcwd()
start_path = current_path + "/" + sys.argv[1]
output_path = current_path + "/" + sys.argv[2]
files = []


for start, dirs, f in os.walk(start_path):
	for fname in f:
		if not fname.startswith('.'):
			files.append(fname)
 



def read_file(file_name):
    with open(file_name) as f:
        return f.readlines()



def cut_list_of_sentences_into_chunks(sentences):
    """takes list of sentences from the file and returns list of N-sized lists
        if the last sublist is not the same size as the other sublists, it is removed from the list
    """
    list_of_lists_of_sentences = []
    for i in range(0, len(sentences), number_of_sentences_per_graph):
        list_of_lists_of_sentences.append(sentences[i:i+number_of_sentences_per_graph])

    if len(list_of_lists_of_sentences[-1]) != number_of_sentences_per_graph:
        del list_of_lists_of_sentences[-1]


    return list_of_lists_of_sentences


    
    


def tokenize_sentences(sentences):
    sents_tokenized = [word_tokenize(sentence.lower()) for sentence in sentences]
    sentences_tokenized = []
    for sent in sents_tokenized:
        words = []
        for word in sent:
            if not all([char in punct for char in word]):
                words.append(word.strip(punct))
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





def write_net_to_graphml(network, fname, number):
    #file = output_path + "/" + "" + fname[:-4] + + ".graphml"
    file = f"{output_path}/{fname[:-4]}_{sys.argv[3]}_{number}.graphml"
    nx.write_graphml(network, file)

        




def main(file_list):
    failed_files = []
    for fname in file_list:
        try:
            print(fname)
            file_name = start_path + "/" + fname
            sentences = read_file(file_name)
            list_of_lists_of_sentences = cut_list_of_sentences_into_chunks(sentences)

            graph_number = 0
            for sublist_of_sentences in list_of_lists_of_sentences:
                try:
                    print(f"Graph number {graph_number} will be made now")
                    if graph_number == max_number_of_graphs_per_language:
                        print("The maximum number of graphs has been made for this language")
                        break
                
                    tokenized_sents = tokenize_sentences(sublist_of_sentences)
                    bigrams = make_bigrams(tokenized_sents)
                    network = make_graph(bigrams)
                    write_net_to_graphml(network, fname, graph_number)
                
                    graph_number += 1
                except Exception:
                    continue
        except UnicodeDecodeError:
            failed_files.append(fname)
            continue
    if failed_files:
        print("Failed files:")
        for f in failed_files:
            print(f)
    return 





main(files)















	