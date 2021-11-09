
import os
import sys
import networkx as nx
import numpy as np



"""provide name of folder with graphs and name of the file where the matrix will be put"""


current_path = os.getcwd()
start_path = current_path + "/" + sys.argv[1]
output_file = current_path + "/" + sys.argv[2]
files = []


for start, dirs, f in os.walk(start_path):
	for fname in f:
		if not fname.startswith('.'):
			files.append(fname)
           



def read_file(file_name):
    graph = nx.read_graphml(file_name)
    return graph




def get_number_of_nodes(graph):
    """returns integer """
    return graph.number_of_nodes()


def get_number_of_edges(graph):
    """returns integer"""
    return graph.number_of_edges()



def get_node_degrees_features(graph):
    """returns list of numbers"""
    degrees = [i[1] for i in list(graph.degree())]
    average_degree = float(np.mean(degrees))
    biggest_degree = max(degrees)
    return [average_degree, biggest_degree]



def get_number_of_stronly_connected_components(graph):
    """returns integer"""
    return nx.number_strongly_connected_components(graph)



def get_ls_features(graph):
    """find largest subnetwork"""
    ls = max(nx.strongly_connected_component_subgraphs(graph), key=len)

    """get percentage of nodes in ls"""
    percentage_of_nodes_in_ls = ls.number_of_nodes() / graph.number_of_nodes()


    """get number of edges"""
    ls_number_of_edges = ls.number_of_edges()

    """edge weights"""
    ls_edge_weights = [e[2] for e in list(ls.edges.data('weight'))]

    """sum of edge weigths"""

    weights_sum = sum(ls_edge_weights)
    average_edge_weight = float(np.mean(ls_edge_weights))
    max_edge_weight = max(ls_edge_weights)


    """node degrees"""

    in_degrees = [i[1] for i in list(ls.in_degree())]
    average_in_degree = float(np.mean(in_degrees))
    max_in_degree = max(in_degrees)

    out_degrees = [i[1] for i in list(ls.out_degree())]
    max_out_degree = max(out_degrees)


    total_degrees = [i[1] for i in list(ls.degree())]
    average_total_degree = float(np.mean(total_degrees))
    max_total_degree = max(total_degrees)


    """small world"""
    average_shortest_path = nx.average_shortest_path_length(ls)
    ls_diameter = nx.diameter(ls)

    ls_undirected = ls.to_undirected()
    avg_clustering = nx.average_clustering(ls_undirected)

    return [percentage_of_nodes_in_ls, ls_number_of_edges, weights_sum, average_edge_weight, max_edge_weight, 
    average_in_degree, max_in_degree, max_out_degree, average_total_degree, max_total_degree, average_shortest_path, 
    ls_diameter, avg_clustering]



def get_all_graph_features(graph):
    """returns list of graph features"""
    features_list = []
    features_list.append(get_number_of_nodes(graph))
    features_list.append(get_number_of_edges(graph))
    features_list.append(get_number_of_stronly_connected_components(graph))
    features_list.extend(get_node_degrees_features(graph))
    features_list.extend(get_ls_features(graph))
    return features_list




def write_array_to_file(nparray):
    """saves feature array as npy file"""
    np.savetxt(output_file, nparray)









def main(file_list):
    failed_files = []
    feature_lists = []
    for fname in file_list:
        try:
            print(fname)
            file_name = start_path + "/" + fname
            graph = read_file(file_name)
            feature_lists.append(get_all_graph_features(graph))
            
        except Exception:
            failed_files.append(fname)
            continue

    feature_tuple = tuple(feature_lists)
    feature_array = np.vstack(feature_tuple)
    write_array_to_file(feature_array)


    if failed_files:
        print("Failed files:")
        for f in failed_files:
            print(f)
    return






main(files)















	