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

if __name__ == "__main__":
    filepath = "../dataset/first.txt"
    separator = file_delimitator(filepath)
    edges = []
    
    with open(filepath, 'r') as file:
        edges = [tuple(map(int, line.strip().split(separator))) for line in file]

    n = len(edges)
    c = int(n*6/100) # Capacity of R_base
    R = edges[:c] # R_base
    tot_triangles = 0

    print(n)
    
    # If we are considering the i-th edge, with i<=c, the formula for the approximation of the number of triangles
    # has 1 at the denominator, thus, we simplify the count by considering all the triangles in R base.
    G = nx.from_edgelist(R)
    tot_triangles = sum(nx.triangles(G).values())/3
    
    # Sampling.
    for i in range(c+1, n):
        p = c/i
        r = random.uniform(0.0, 1.0)
        sampled = False
        if r < p:
            # Remove a random edge.
            e = list(G.edges)
            chosen_edge = random.choice(e)
            G.remove_edge(chosen_edge[0], chosen_edge[1])

            # Add edge to graph.
            u, v = edges[i]
            G.add_edge(u, v)
            sampled = True
        
        # Count triangles.
        if sampled == False:
            u, v = edges[i]
            G.add_edge(u, v)

        triangles = 0
        prob = (c/i-1)**2

        # Count the number of triangles in which the edge (u,v) is involved.
        for w in set(G.neighbors(u)).intersection(G.neighbors(v)):
            triangles += 1
        
        # Remove (u,v) from G if it was not sample.
        if sampled == False:
            G.remove_edge(u, v)

        tot_triangles += triangles/prob

    tot_triangles = int(tot_triangles)

    print("Totale number of triangles: {:,}".format(tot_triangles))

    # Save the result (number of edges and approximate number of triangles) in the file
    with open("result.txt", "a") as file:
        file.write(str(n) + " " + str(triangles) + "\n")

    print("Result saved!")