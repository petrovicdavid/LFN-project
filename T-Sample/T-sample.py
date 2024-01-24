# Andrea Ghiotto 2118418, David Petrovic 2092073
# Learning From Network project
# Implementation of T-sample algorithm

import numpy as np
import networkx as nx
import random

def file_delimitator(filename):
    with open(filename, 'r') as file:
        first_rows = [file.readline() for _ in range(2)]  # Read the first two rows

    # Verify if there is at least one tab in the first two rows.
    tab = any('\t' in row for row in first_rows)

    # Return the correct delimatator.
    return '\t' if tab else ' '

def get_dataset(filename):
    filename = filename.replace("../dataset/", "")
    return filename

def number_generator():
    number = 0
    while number == 0:
        number = random.uniform(0, 1)
    return number

if __name__ == "__main__":
    filepath = "../dataset/first.txt"
    separator = file_delimitator(filepath)
    edges_file = []
    
    with open(filepath, 'r') as file:
        edges_file = [tuple(map(int, line.strip().split(separator))) for line in file]

    edges = len(edges_file)
    c = 2165 # Capacity of R_base for the first dataset
    #c = 5647 # Capacity of R_base for the second dataset
    R = edges_file[:c] # R_base
    triangles = 0

    print("Number of edges: " + str(edges))
    
    # If we are considering the i-th edge, with i<=c, the formula for the approximation of the number of triangles
    # has 1 at the denominator, thus, we simplify the count by considering all the triangles in R_base.
    G = nx.from_edgelist(R)
    triangles = sum(nx.triangles(G).values())/3
    
    # Sampling.
    for i in range(c+1, edges):
        p = c/i
        r = number_generator()
        sampled = False
        if r < p:
            # Remove a random edge.
            e = list(G.edges)
            chosen_edge = random.choice(e)
            G.remove_edge(chosen_edge[0], chosen_edge[1])

            # Add edge to graph.
            u, v = edges_file[i]
            G.add_edge(u, v)
            sampled = True
        
        # Count triangles.
        if sampled == False:
            u, v = edges_file[i]
            G.add_edge(u, v)

        t = 0
        prob = (c/i-1)**2

        # Count the number of triangles in which the edge (u,v) is involved.
        for w in set(G.neighbors(u)).intersection(G.neighbors(v)):
            t += 1
        
        # Remove (u,v) from G if it was not sampled.
        if sampled == False:
            G.remove_edge(u, v)

        triangles += t/prob

    triangles = int(triangles)

    print("Approximate number of triangles: {:,}".format(triangles))

    # Save the results (number of edges and approximate number of triangles) in the result file.
    result_file = "result_" + get_dataset(filepath)
    with open(result_file, "a") as file:
        file.write(str(edges) + " " + str(triangles) + "\n")

    print("Results saved!")