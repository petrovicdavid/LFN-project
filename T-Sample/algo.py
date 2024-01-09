import numpy as np
import networkx as nx
import random

if __name__ == "__main__":
    filepath = "input.txt"
    separator = ' '
    #separator = '\t'
    edges = []
    
    with open(filepath, 'r') as file:
        edges = [tuple(map(int, line.strip().split(separator))) for line in file]

    n = len(edges)
    #c = 50000
    c = int(n*6/100) # capacity of R base
    R = edges[:c] # R base
    tot_triangles = 0

    print(n)
    
    # since the formula for the approximation of the number of triangles has 1 at
    # the denominator, we just count all the triangles in R base
    G = nx.from_edgelist(R)
    tot_triangles = sum(nx.triangles(G).values())/3
    

    # Sampling
    for i in range(c+1, n):
        p = c/i
        r = random.uniform(0.0, 1.0)
        sampled = False
        if r < p:
            # Remove a random edge
            e = list(G.edges)
            chosen_edge = random.choice(e)
            G.remove_edge(chosen_edge[0], chosen_edge[1])

            # Add edge to graph
            u, v = edges[i]
            G.add_edge(u, v)
            sampled = True
        
        # Count triangles
        if sampled == False:
            u, v = edges[i]
            G.add_edge(u, v)

        triangles = 0
        prob = (c/i-1)**2

        # Count the number of triangles in which the edge (u,v) is involved
        for w in set(G.neighbors(u)).intersection(G.neighbors(v)):
            triangles += 1
        
        # Remove (u,v) from G if it was not sample
        if sampled == False:
            G.remove_edge(u, v)

        tot_triangles += triangles/prob


    tot_triangles = int(tot_triangles)

    print("Sampling done")
    print("Tot_triangles: {:,}".format(tot_triangles))
