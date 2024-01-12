# Andrea Ghiotto 2118418, David Petrovic 2092073
# Learning From Network project
# Implementation of the computation of the clustering coefficients

import scipy.special

if __name__ == "__main__":
    filepath_eigen = "../eigenTriangle/result.txt"
    filepath_samp = "../T-Sample/result.txt"
    separator = " "
    
    with open(filepath_eigen, 'r') as file:
        results_eigen = [tuple(map(int, line.strip().split(separator)[:2])) for line in file]

    clustering_coefficients = []

    for tupla in results_eigen:
        print(tupla)
        number_edges, number_triangles = tupla
        
        cc = number_triangles / (6*scipy.special.binom(number_edges, 3))
        clustering_coefficients.append((cc, number_edges))

    # Save the result (number of edges and approximate number of triangles) in the file
    with open("result.txt", "a") as file:
        for tupla in clustering_coefficients:
            file.write(str(tupla[0]) + " " + str(tupla[1]) + "\n")

    print("Result saved!")